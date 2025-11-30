from backend.database import Database

class MeasurementService:
    def __init__(self):
        self.db = Database()
    
    def add_measurement(self, name, code, measurement_type, base_unit, conversion_factor, description=""):
        """Add new measurement unit"""
        with self.db.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute('''
                INSERT INTO measurements (name, code, type, base_unit, conversion_factor, description)
                VALUES (?, ?, ?, ?, ?, ?)
            ''', (name, code, measurement_type, base_unit, conversion_factor, description))
            conn.commit()
            return cursor.lastrowid
    
    def get_all_measurements(self):
        """Get all measurement units"""
        with self.db.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute('SELECT * FROM measurements ORDER BY type, name')
            return cursor.fetchall()
    
    def get_measurements_by_type(self, measurement_type):
        """Get measurements by type"""
        with self.db.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute('SELECT * FROM measurements WHERE type = ? ORDER BY name', (measurement_type,))
            return cursor.fetchall()
    
    def delete_measurement(self, measurement_id):
        """Delete measurement unit"""
        with self.db.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute('DELETE FROM measurements WHERE id = ?', (measurement_id,))
            conn.commit()
            return cursor.rowcount