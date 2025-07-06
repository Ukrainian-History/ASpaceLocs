Flask app to view and/or manage ArchivesSpace locations and top containers.

To run in production:

```
docker build -t aspacelocs .
docker run -d -p 8000:8000 aspacelocs
```
