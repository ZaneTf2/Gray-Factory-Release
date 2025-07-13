class VPKError(Exception):
    """Base exception for VPK-related errors"""
    pass

class VPKParseError(VPKError):
    """Error when parsing VPK file structure"""
    pass

class VPKFileNotFoundError(VPKError):
    """Error when requested file is not found in VPK"""
    pass
