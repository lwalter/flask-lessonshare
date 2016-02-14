Flask-Lessonshare
=================
Lessonshare is a web application built to allow educators across the world create, share, and collaborate on educational material. The backend is written in Python and [Flask](http://flask.pocoo.org/) and the frontend is [Angular-Material](https://material.angularjs.org/latest/).

Contributing
------------
* Issue tracking
    * For any proposed features or bugs, please open an issue to allow for tracking of the item.

* Submitting changes
    * Fork the repository and switch to a new branch with `git checkout -b <branch-name>`
    * Make all necessary changes and submit a new pull request. Please provide detailed information to help facilitate understanding of the changes. Reference the issue that the pull request applies to.
    * After a code review, the pull request will either be accepted or rejected.

Installation
------------
* [Vagrant](https://www.vagrantup.com/) is used for a standard development environment, please ensure this is installed.
* Clone the repository and navigate to the vagrant directory.
* Run `vagrant up`, this may take some time to provision the virtual machine.
    * Guest port 5000 and host port 5000 are forwarded to access the application.
    * Guest port 15432 and host port 5432 are forwarded to access the PostgreSQL database.
    * The repository on the host will be shared to /flask-lessonshare of the guest environment.
    * A Python virtualenv will be created in the /flask-lessonshare directory called flask.
* After the machine has been provisioned you may run `vagrant ssh` to the environment in order to run the application.
    * Take advantage of the virtualenv by running the application using `/flask-lessonshare/flask/bin/python run.py`
    * New pip packages can be installed by running `/flask-lessonshare/flask/bin/pip install <package name>`