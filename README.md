# RESTful API for social media with help DRF

## Features
<hr>

- CRUD users
- Filter users by username/email
- Follow/Unfollow other users
- CRUD for posts with tags
- Filter posts by tags/author
- Like/Dislike for posts
- Comment posts


## Local Run
<hr>

```shell
git clone https://github.com/usrofgh/social_media.git
cd social_media
python -m venv venv

(windows) -> venv\Scripts\activate
(linux) -> source venv/bin/activate

pip install -r requirements.txt
python manage.py runserver
```

### Endpoints
<hr>

![endpoints.png](imgs%2Fendpoints.png)
### Schema
<hr>

![schema.png](imgs%2Fschema.png)