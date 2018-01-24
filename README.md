# Stuy-n-Large

Stuy n' Buy<br>
Edward Luo, Ryan Siu, Max Korsun, Andrew Wong<br>
Software Development Project 02<br>
Period 09

## Description
Stuy n' Buy is a web application for members of the Stuyvesant community to buy and sell items they no longer need. Members may put up items for sale with a name, price, description, and picture, or let others know what items they're looking for. Other users may search for items, and contact the seller if they are interested in an item.

Video tutorial: [Stuy n' Buy](https://www.youtube.com/watch?v=nN3dwb9bchs&feature=youtu.be)

## Setup

### Dependencies
Stuy n' Buy requires certain python libraries to run. You can install the libraries using the command below:
```
$ pip install --upgrade requests google-auth google-auth-oauthlib google-auth-httplib2 google-api-python-client
```

### API Keys
Place the procured `client_secret.json` file in the root directory of the application.

### Running
Simply run 
```
$ python main.py
```
in a terminal, then go to `localhost:5000` in any browser.

### Database
A freshly cloned version of this project should include a test database and sample images. If you would like to create a new database, you can run the following commands from the root directory of the application:
```
$ rm data/database.db
$ rm static/data/img/*.jpg
$ python utils/db.py
```

## Usage
Please watch the video for a visual stepthrough of using the website. Users will first have to create an account before they can buy or sell items on the website. They can list items to be sold or items they're looking for by "creating" an item on the "Marketplace" page. A user that has listed items can then mark their items as "Meeting Arranged", or in progress, "Sold", or "Available", meaning it is listed on the default marketplace. Users can also contact the sellers or buyers of items in the marketplace by sending them a message on the item-specific page.

If you would like to test this website with already-generated accounts, please refer to the below table for login information.

| Username           | Password | Admin |
|--------------------|----------|-------|
| `rsiu@stuy.edu`    | a        | True  |
| `mkorsun@stuy.edu` | a        | False |
| `jdoe@stuy.edu`    | a        | False |

If you have any other questions, feel free to look at our FAQ page on the website!

## Notes
File uploading may not work on all operating systems. It has been tested to work on Ubuntu.
