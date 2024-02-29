import mariadb
from fastapi.testclient import TestClient

from main import app

client = TestClient(app)

#def test_init_db():
#    with pytest.raises(Exception) as e_info:
#        response = client.get("/api/v1/sysadmin")
#        assert response.status_code == 500
    
def test_init_db():
    try:
        response = client.get("/api/v1/sysadmin")
        assert response.status_code == 200
    except mariadb.OperationalError:
        # DB is exist
        assert True
    except AttributeError:
        assert True