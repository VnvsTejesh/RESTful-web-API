import json
import mysql.connector
import redis
import time
import tornado.web
import uuid
import asyncio

# Redis cache connection
redis_client = redis.Redis(host='localhost', port=6379, db=0)

# MySQL database connection
db_conn = mysql.connector.connect(
    host='localhost',
    user='root',
    password='',
    database='guids'
)

# Tornado request handlers
class GuidHandler(tornado.web.RequestHandler):

    def post(self, guid=None):
        if guid is None:
            guid = str(uuid.uuid4()).replace('-', '').upper()
        
        data = json.loads(self.request.body)
        expire = data.get('expire')
        metadata = {
            'guid': guid,
            'expire': data.get('expire', self._get_default_expiry()),
            'user': data['user']
        }
        
        # Store GUID and metadata in MySQL
        self._store_metadata_in_mysql(metadata)
        
        # Store GUID and metadata in cache
        if expire is not None:
            redis_client.set(guid, json.dumps(metadata), ex=expire)
        else:
            redis_client.set(guid, json.dumps(metadata), ex=self._get_cache_expiry())
        
        self.write(json.dumps(metadata))

    def get(self, guid):
        # Check if GUID is in cache
        metadata = redis_client.get(guid)
        if metadata is not None:
            self.write(metadata.decode())
        else:
            # GUID not in cache, fetch from MySQL
            metadata = self._fetch_metadata_from_mysql(guid)
            if metadata is not None:
                # Store GUID and metadata in cache for future use
                redis_client.set(guid, metadata, ex=self._get_cache_expiry())
                self.write(metadata)
            else:
                self.set_status(404)
        
    def put(self, guid):
        data = json.loads(self.request.body)
        expire = data.get('expire')
        
        # Update metadata in MySQL
        self._update_metadata_in_mysql(guid, expire)
        
        # Update metadata in cache
        metadata = self._fetch_metadata_from_mysql(guid)
        if metadata is not None:
            redis_client.set(guid, metadata, ex=expire)
        self.write(metadata)
        
    def delete(self, guid):
        # Delete GUID from MySQL
        self._delete_metadata_from_mysql(guid)
        
        # Delete GUID from cache
        redis_client.delete(guid)
    
    def _fetch_metadata_from_mysql(self, guid):
        cursor = db_conn.cursor()
        query = 'SELECT * FROM metadata WHERE guid=%s'
        cursor.execute(query, (guid,))
        result = cursor.fetchone()
        cursor.close()
        
        if result is not None:
            return json.dumps({
                'guid': result[0],
                'expire': result[1],
                'user': result[2]
            })
        
        return None
    
    def _store_metadata_in_mysql(self, metadata):
        cursor = db_conn.cursor()
        query = 'INSERT INTO metadata (guid, expire, user) VALUES (%s, %s, %s)'
        cursor.execute(query, (metadata['guid'], metadata['expire'], metadata['user']))
        db_conn.commit()
        cursor.close()
        
    def _update_metadata_in_mysql(self, guid, expire):
        cursor = db_conn.cursor()
        query = 'UPDATE metadata SET expire=%s WHERE guid=%s'
        cursor.execute(query, (expire, guid))
        db_conn.commit()
        cursor.close()
        
    def _delete_metadata_from_mysql(self, guid):
        cursor = db_conn.cursor()
        query = 'DELETE FROM metadata WHERE guid=%s'
        cursor.execute(query, (guid,))
        db_conn.commit()
        cursor.close()
    
    def _get_cache_expiry(self):
        return int(time.time()) + (30 * 24 * 60 * 60)  # 30 days
    
    def _get_default_expiry(self):
        return int(time.time()) + (30 * 24 * 60 * 60)  # 30 days


# Tornado application settings and routes
def make_app():
    return tornado.web.Application([
        (r'/guid/([\dA-F]{32})', GuidHandler),
        (r'/guid', GuidHandler)
    ])
async def main():
    app = make_app()
    app.listen(8000)
    #tornado.ioloop.IOLoop.current().start()
    shutdown_event = asyncio.Event()
    await shutdown_event.wait()

if __name__ == '__main__':
    asyncio.run(main())
    # main()


