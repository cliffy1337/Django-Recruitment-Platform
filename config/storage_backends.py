from django.conf import settings
from storages.backends.s3boto3 import S3Boto3Storage

class MediaStorage(S3Boto3Storage):
    """Storage for general media files (resumes, documents, etc.)"""
    location = 'media'
    file_overwrite = False
    default_acl = 'private'
    
    def url(self, name, expire=None):
        """Generate a presigned URL for secure access"""
        if expire is None:
            expire = getattr(settings, 'AWS_QUERYSTRING_EXPIRE', 3600)
        
        # Generate presigned URL for private files
        return self.connection.meta.client.generate_presigned_url(
            'get_object',
            Params={
                'Bucket': self.bucket.name,
                'Key': self._get_key(name)
            },
            ExpiresIn=expire
        )
    
    def _get_key(self, name):
        """Get the full key path"""
        if self.location:
            return f"{self.location}/{name}"
        return name


class ProfilePictureStorage(S3Boto3Storage):
    """Storage for profile pictures with CloudFront CDN support"""
    location = 'profile_pictures'
    file_overwrite = True  # Overwrite when updating profile picture
    default_acl = 'public-read'
    
    def url(self, name):
        """Return CloudFront URL if configured, otherwise S3 URL"""
        # If CloudFront is configured, use it for faster delivery
        if hasattr(settings, 'AWS_CLOUDFRONT_DOMAIN') and settings.AWS_CLOUDFRONT_DOMAIN:
            return f"https://{settings.AWS_CLOUDFRONT_DOMAIN}/{self.location}/{name}"
        
        # Fallback to S3 URL
        if self.custom_domain:
            return f"https://{self.custom_domain}/{self.location}/{name}"
        
        return super().url(name)


class ResumeStorage(S3Boto3Storage):
    """Specialized storage for resumes with enhanced security"""
    location = 'resumes'
    file_overwrite = False
    default_acl = 'private'
    
    def url(self, name, expire=None):
        """Generate a presigned URL for resume access"""
        if expire is None:
            expire = getattr(settings, 'AWS_QUERYSTRING_EXPIRE', 3600)
        
        # Shorter expiration for sensitive resume files
        resume_expire = getattr(settings, 'AWS_RESUME_URL_EXPIRE', 1800)  # 30 minutes default
        
        return self.connection.meta.client.generate_presigned_url(
            'get_object',
            Params={
                'Bucket': self.bucket.name,
                'Key': self._get_key(name)
            },
            ExpiresIn=resume_expire
        )
    
    def _get_key(self, name):
        """Get the full key path with user isolation"""
        if self.location:
            return f"{self.location}/{name}"
        return name


class ApplicationDocumentStorage(S3Boto3Storage):
    """Storage for application-specific documents"""
    location = 'applications'
    file_overwrite = False
    default_acl = 'private'
    
    def url(self, name, expire=None):
        """Generate a presigned URL for application documents"""
        if expire is None:
            expire = getattr(settings, 'AWS_QUERYSTRING_EXPIRE', 3600)
        
        return self.connection.meta.client.generate_presigned_url(
            'get_object',
            Params={
                'Bucket': self.bucket.name,
                'Key': self._get_key(name)
            },
            ExpiresIn=expire
        )
    
    def _get_key(self, name):
        """Get the full key path"""
        if self.location:
            return f"{self.location}/{name}"
        return name