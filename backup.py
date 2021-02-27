class BackupFile:
    """Simple backup rotation and retention policy class"""
    
    def __init__(self):
        self.retention_policies = []
        self.retention_total = int(400)
        self.retention_daily = int(100)
        self.retention_weekly = int(100)
        self.retention_monthly = int(100)
        self.retention_yearly = int(100)
        self.file_list = []
        self.retention_policies = []

