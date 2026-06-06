import time
from datetime import datetime, timedelta

def format_time(seconds):
    """format seconds to readable time"""
    if seconds < 60:
        return f"{int(seconds)}s"
    elif seconds < 3600:
        mins = int(seconds // 60)
        secs = int(seconds % 60)
        return f"{mins}m {secs}s"
    else:
        hours = int(seconds // 3600)
        mins = int((seconds % 3600) // 60)
        return f"{hours}h {mins}m"

def calculate_eta(processed, total, elapsed_time):
    """calculate estimated time of arrival"""
    if processed == 0:
        return "calculating..."
    
    speed = processed / elapsed_time
    remaining = total - processed
    eta_seconds = remaining / speed if speed > 0 else 0
    
    return format_time(eta_seconds)

def calculate_progress(current, total):
    """calculate progress percentage"""
    if total == 0:
        return 0
    return round((current / total) * 100, 2)

def get_progress_bar(percentage, length=10):
    """get visual progress bar"""
    filled = int(length * percentage / 100)
    bar = "█" * filled + "░" * (length - filled)
    return f"[{bar}] {percentage}%"

class ForwardingStats:
    def __init__(self):
        self.total_fetched = 0
        self.successful = 0
        self.failed = 0
        self.start_time = time.time()
        self.messages_received = 0
        self.messages_sent = 0
        self.in_queue = 0
        self.is_paused = False
        self.is_stopped = False
    
    def update(self, successful=0, failed=0, fetched=0):
        """update statistics"""
        self.successful += successful
        self.failed += failed
        self.total_fetched += fetched
        self.messages_sent += successful
    
    def get_elapsed_time(self):
        """get elapsed time"""
        return time.time() - self.start_time
    
    def get_speed(self):
        """calculate current speed"""
        elapsed = self.get_elapsed_time()
        if elapsed == 0:
            return 0
        return round(self.messages_sent / elapsed, 2)
    
    def get_eta(self, total_messages):
        """get estimated time"""
        return calculate_eta(self.messages_sent, total_messages, self.get_elapsed_time())
    
    def get_progress(self, total_messages):
        """get progress percentage"""
        return calculate_progress(self.messages_sent, total_messages)
    
    def get_success_rate(self):
        """calculate success rate"""
        total = self.successful + self.failed
        if total == 0:
            return 0
        return round((self.successful / total) * 100, 2)
    
    def to_dict(self):
        """convert stats to dictionary"""
        elapsed = self.get_elapsed_time()
        return {
            'status': 'paused' if self.is_paused else ('stopped' if self.is_stopped else 'running'),
            'total_fetched': self.total_fetched,
            'successful': self.successful,
            'failed': self.failed,
            'success_rate': self.get_success_rate(),
            'speed': self.get_speed(),
            'elapsed_time': format_time(elapsed),
            'eta': 'paused' if self.is_paused else 'calculating...',
            'progress': 0,
            'received': self.messages_received,
            'sent': self.messages_sent,
            'in_queue': self.in_queue
        }
