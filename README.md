# <ins> Social-media-app-backend </ins>

## <ins> Description </ins>
the backend api containing all http endpoints to the front end application.
Use `python manage.py runserver` to start development enviornment. 

**end-points:**
- `http://127.0.0.1:8000` : Home
- `http://127.0.0.1:8000/admin` : Admin/Superuser panel to access data
- `http://127.0.0.1:8000/auth/signup` : Send *POST* requests here to create new Users
- `http://127.0.0.1:8000/auth/login` : Send *POST* request consisting of (username, login) to receiver auth token
- `http://127.0.0.1:8000/auth/loginData` : Send *POST* request here containg email or phone number to receive username back.****

---

## Project Details
* <ins>Name</ins> :  Social-Media-App-Backend
* <ins>Category</ins> :  Python/Django
* <ins>Application Type</ins> :  Backend Server
* <ins>Default URL</ins> :  http://127.0.0.1:8000

---

### Packages Used ###
| name                  | PyPi Links                                                               |
| --------------------- | ------------------------------------------------------------------------ |
| Django                | [django PyPi](https://pypi.org/project/Django/)                          |
| Django Rest Framework | [djangorestframework PyPi](https://pypi.org/project/djangorestframework) |

