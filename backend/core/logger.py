import logging
import sys
import json
from datetime import datetime
from core.config import settings

class JsonFormatter(logging.Formatter):
    """
    Logları JSON formatında çıktılayan özel formatlayıcı.
    Kibana/ELK veya CloudWatch gibi sistemler için idealdir.
    """
    def format(self, record):
        log_record = {
            "timestamp": datetime.utcnow().isoformat(),
            "level": record.levelname,
            "logger": record.name,
            "message": record.getMessage(),
            "module": record.module,
            "func": record.funcName,
            "line": record.lineno
        }
        
        # Hata varsa ekle
        if record.exc_info:
            log_record["exception"] = self.formatException(record.exc_info)
            
        # Extra alanlar varsa ekle (request_id vb.)
        if hasattr(record, "request_id"):
            log_record["request_id"] = record.request_id
            
        return json.dumps(log_record)

def configure_logging():
    """
    Python logging modülünü JSON formatında yapılandırır.
    """
    root_logger = logging.getLogger()
    
    # Önceki handler'ları temizle (Çift logu önle)
    if root_logger.handlers:
        for handler in root_logger.handlers:
            root_logger.removeHandler(handler)
            
    handler = logging.StreamHandler(sys.stdout)
    handler.setFormatter(JsonFormatter())
    
    root_logger.setLevel(logging.INFO)
    root_logger.addHandler(handler)
    
    # Kütüphane gürültüsünü azalt
    logging.getLogger("uvicorn.access").setLevel(logging.WARNING)
    logging.getLogger("sqlalchemy.engine").setLevel(logging.WARNING)
    
    # Test modunda debug aç
    if settings.TESTING:
        root_logger.setLevel(logging.DEBUG)

# Varsayılan logger nesnesi
logger = logging.getLogger("retail_dss")
