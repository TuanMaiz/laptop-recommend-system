"""
Fingerprint utilities for handling external fingerprints from various sources
"""

import uuid
import time
from typing import Optional, Dict, Any
from fastapi import Request, Header, Cookie
import logging

logger = logging.getLogger(__name__)


class FingerprintManager:
    """Manages external fingerprints and generates consistent hashes"""
    
    @staticmethod
    def generate_fingerprint_hash(fingerprint: str) -> str:
        """
        Generate consistent SHA256 hash for external fingerprint
        
        Args:
            fingerprint: External fingerprint string (browser fingerprint, device ID, etc.)
            
        Returns:
            SHA256 hash string
            
        Raises:
            ValueError: If fingerprint is empty or invalid
        """
        if not fingerprint or not isinstance(fingerprint, str):
            raise ValueError("Fingerprint must be a non-empty string")
        
        # Clean and normalize fingerprint
        cleaned_fingerprint = fingerprint.strip()
        if not cleaned_fingerprint:
            raise ValueError("Fingerprint cannot be empty or whitespace only")
        
        # Generate SHA256 hash
        return hashlib.sha256(cleaned_fingerprint.encode()).hexdigest()
    
    @staticmethod
    def generate_session_fingerprint() -> str:
        """
        Generate a new session fingerprint (used when no external fingerprint available)
        
        Returns:
            New unique fingerprint string
        """
        return f"session_{uuid.uuid4().hex}_{int(time.time())}"
    
    @staticmethod
    def extract_fingerprint_from_request(
        request: Request,
        fingerprint_header: Optional[str] = None,
        fingerprint_cookie: Optional[str] = None,
        user_agent: Optional[str] = None
    ) -> str:
        """
        Extract fingerprint from various request sources
        
        Args:
            request: FastAPI request object
            fingerprint_header: Header name containing fingerprint
            fingerprint_cookie: Cookie name containing fingerprint
            user_agent: User agent string (fallback)
            
        Returns:
            Fingerprint string or generated session fingerprint
        """
        # Try to get fingerprint from header
        if fingerprint_header:
            header_value = request.headers.get(fingerprint_header)
            if header_value:
                logger.debug(f"Found fingerprint in header: {fingerprint_header}")
                return header_value
        
        # Try to get fingerprint from cookie
        if fingerprint_cookie:
            cookie_value = request.cookies.get(fingerprint_cookie)
            if cookie_value:
                logger.debug(f"Found fingerprint in cookie: {fingerprint_cookie}")
                return cookie_value
        
        # Try to get from request parameters
        if hasattr(request, 'query_params'):
            param_value = request.query_params.get('fingerprint')
            if param_value:
                logger.debug("Found fingerprint in query parameters")
                return param_value
        
        # Fallback to user agent + IP (not perfect but better than nothing)
        if user_agent:
            ip = getattr(request, 'client', {}).get('host', 'unknown')
            fallback_fingerprint = f"{user_agent}_{ip}"
            logger.debug(f"Generated fallback fingerprint from user agent and IP")
            return fallback_fingerprint
        
        # Generate new session fingerprint
        session_fingerprint = FingerprintManager.generate_session_fingerprint()
        logger.debug(f"Generated new session fingerprint: {session_fingerprint[:16]}...")
        return session_fingerprint


class FingerprintMiddleware:
    """
    FastAPI middleware to automatically extract and attach fingerprints to requests
    """
    
    def __init__(self, app, header_name: str = "X-Fingerprint", cookie_name: str = "laptop_fingerprint"):
        self.app = app
        self.header_name = header_name
        self.cookie_name = cookie_name
        self.fingerprint_attr = "_fingerprint"
        
        # Add middleware to the app
        app.middleware("http")(self.middleware_function)
    
    async def middleware_function(self, request: Request, call_next):
        """Extract fingerprint and add to request state"""
        try:
            # Extract fingerprint from various sources
            fingerprint = FingerprintManager.extract_fingerprint_from_request(
                request,
                fingerprint_header=self.header_name,
                fingerprint_cookie=self.cookie_name,
                user_agent=request.headers.get("user-agent")
            )
            
            # Add fingerprint to request state
            request.state.fingerprint = fingerprint
            request.state.fingerprint_hash = FingerprintManager.generate_fingerprint_hash(fingerprint)
            
            logger.debug(f"Processed fingerprint: {fingerprint[:16]}...")
            
        except Exception as e:
            logger.error(f"Error processing fingerprint: {e}")
            # Use default fingerprint if error occurs
            default_fingerprint = FingerprintManager.generate_session_fingerprint()
            request.state.fingerprint = default_fingerprint
            request.state.fingerprint_hash = FingerprintManager.generate_fingerprint_hash(default_fingerprint)
        
        response = await call_next(request)
        return response


def get_fingerprint_from_request(request: Request) -> str:
    """
    Get fingerprint from FastAPI request (after middleware processing)
    
    Args:
        request: FastAPI request object
        
    Returns:
        Fingerprint string
    """
    return getattr(request.state, 'fingerprint', FingerprintManager.generate_session_fingerprint())


def get_fingerprint_hash_from_request(request: Request) -> str:
    """
    Get fingerprint hash from FastAPI request (after middleware processing)
    
    Args:
        request: FastAPI request object
        
    Returns:
        Fingerprint hash string
    """
    return getattr(request.state, 'fingerprint_hash', 
                  FingerprintManager.generate_fingerprint_hash(
                      FingerprintManager.generate_session_fingerprint()
                  ))


# Dependency injection for FastAPI
def get_fingerprint_dependency(request: Request) -> str:
    """
    FastAPI dependency to get fingerprint from request
    
    Usage:
        @app.get("/endpoint")
        def endpoint(fingerprint: str = Depends(get_fingerprint_dependency)):
            # Use fingerprint here
    """
    return get_fingerprint_from_request(request)


def get_fingerprint_hash_dependency(request: Request) -> str:
    """
    FastAPI dependency to get fingerprint hash from request
    
    Usage:
        @app.get("/endpoint")
        def endpoint(fingerprint_hash: str = Depends(get_fingerprint_hash_dependency)):
            # Use fingerprint hash here
    """
    return get_fingerprint_hash_from_request(request)