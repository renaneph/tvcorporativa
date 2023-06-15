from os import system


"""
0 - error
1 - done
2 - already satisfied
"""


def setup():
    result = 0

    #try to init and migrate database
    try:
        system("python3 manage.py makemigrations")
        system("python3 manage.py migrate")
        system("python3 manage.py createsuperuser --noinput --email=gpr@gpr.com.br")
        system("python3 manage.py loaddata user.json")
        result = 1

    except Exception as e:
        result = 0

    return result


if __name__ == "__main__":

    result = setup()

    system("python3 manage.py runserver 0.0.0.0:8000 &")
