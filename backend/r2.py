#!/usr/bin/env python3
"""
Brain Circuit Atlas - Cloudflare R2 Storage Client
Implements S3 Signature Version 4 using only Python's standard library (no pip required).
Compatible with Cloudflare R2 free tier (10 GB storage, $0 egress fees).
"""
import os
import hmac
import hashlib
import datetime
import urllib.request
import urllib.parse
import urllib.error
import mimetypes

def sign(key, msg):
    return hmac.new(key, msg.encode('utf-8'), hashlib.sha256).digest()

def get_signature_key(key, date_stamp, region_name, service_name):
    k_date = sign(('AWS4' + key).encode('utf-8'), date_stamp)
    k_region = sign(k_date, region_name)
    k_service = sign(k_region, service_name)
    k_signing = sign(k_service, 'aws4_request')
    return k_signing

class CloudflareR2:
    def __init__(self, account_id, access_key_id, secret_access_key, bucket_name, public_url=None):
        self.account_id = account_id.strip() if account_id else ''
        self.access_key_id = access_key_id.strip() if access_key_id else ''
        self.secret_access_key = secret_access_key.strip() if secret_access_key else ''
        self.bucket_name = bucket_name.strip() if bucket_name else ''
        self.public_url = public_url.strip().rstrip('/') if public_url else None
        self.region = 'auto'
        self.service = 's3'

    def is_configured(self):
        return bool(self.account_id and self.access_key_id and self.secret_access_key and self.bucket_name)

    def _get_host(self):
        return f"{self.account_id}.r2.cloudflarestorage.com"

    def _get_endpoint(self):
        return f"https://{self._get_host()}"

    def _request(self, method, key="", payload=b"", extra_headers=None, query_params=None):
        if not self.is_configured():
            raise ValueError("Cloudflare R2 is not configured. Missing credentials.")

        host = self._get_host()
        now = datetime.datetime.utcnow()
        amz_date = now.strftime('%Y%m%dT%H%M%SZ')
        date_stamp = now.strftime('%Y%m%d')

        canonical_uri = '/' + self.bucket_name
        if key:
            canonical_uri += '/' + urllib.parse.quote(key.lstrip('/'), safe='-_.~')

        canonical_querystrings = ''
        if query_params:
            canonical_querystrings = urllib.parse.urlencode(sorted(query_params.items()))

        payload_hash = hashlib.sha256(payload).hexdigest()

        headers = {
            'host': host,
            'x-amz-date': amz_date,
            'x-amz-content-sha256': payload_hash,
        }
        if extra_headers:
            for k, v in extra_headers.items():
                headers[k.lower()] = v

        canonical_headers = "".join(f"{k}:{headers[k]}\n" for k in sorted(headers.keys()))
        signed_headers = ";".join(sorted(headers.keys()))

        canonical_request = (
            f"{method}\n"
            f"{canonical_uri}\n"
            f"{canonical_querystrings}\n"
            f"{canonical_headers}\n"
            f"{signed_headers}\n"
            f"{payload_hash}"
        )

        algorithm = 'AWS4-HMAC-SHA256'
        credential_scope = f"{date_stamp}/{self.region}/{self.service}/aws4_request"
        string_to_sign = (
            f"{algorithm}\n"
            f"{amz_date}\n"
            f"{credential_scope}\n"
            f"{hashlib.sha256(canonical_request.encode('utf-8')).hexdigest()}"
        )

        signing_key = get_signature_key(self.secret_access_key, date_stamp, self.region, self.service)
        signature = hmac.new(signing_key, string_to_sign.encode('utf-8'), hashlib.sha256).hexdigest()

        authorization_header = (
            f"{algorithm} Credential={self.access_key_id}/{credential_scope}, "
            f"SignedHeaders={signed_headers}, Signature={signature}"
        )
        headers['Authorization'] = authorization_header

        url = f"{self._get_endpoint()}{canonical_uri}"
        if canonical_querystrings:
            url += f"?{canonical_querystrings}"

        req = urllib.request.Request(url, data=payload if method in ['PUT', 'POST'] else None, headers=headers, method=method)
        with urllib.request.urlopen(req, timeout=30) as resp:
            return resp.read()

    def test_connection(self):
        """Tests bucket access with a HEAD request."""
        try:
            self._request('HEAD')
            return {"ok": True, "message": f"Successfully connected to bucket '{self.bucket_name}'."}
        except urllib.error.HTTPError as e:
            return {"ok": False, "message": f"HTTP {e.code}: {e.reason}"}
        except Exception as e:
            return {"ok": False, "message": str(e)}

    def upload_file(self, local_path, remote_key=None, content_type=None):
        """Uploads a local file to R2."""
        if not remote_key:
            remote_key = os.path.basename(local_path)
        if not content_type:
            content_type, _ = mimetypes.guess_type(local_path)
            content_type = content_type or 'application/octet-stream'

        with open(local_path, 'rb') as f:
            data = f.read()

        extra_headers = {'content-type': content_type}
        self._request('PUT', key=remote_key, payload=data, extra_headers=extra_headers)

        pub_url = f"{self.public_url}/{remote_key}" if self.public_url else None
        return {
            "remote_key": remote_key,
            "bytes": len(data),
            "public_url": pub_url,
            "uploaded": True
        }

    def download_file(self, remote_key, local_path):
        """Downloads an object from R2 to a local destination."""
        data = self._request('GET', key=remote_key)
        os.makedirs(os.path.dirname(os.path.abspath(local_path)), exist_ok=True)
        with open(local_path, 'wb') as f:
            f.write(data)
        return {"remote_key": remote_key, "bytes": len(data), "downloaded": True}
