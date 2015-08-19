# Watchguard Tool

## TL;DR

This is a tool for the irritating watchguard problem on GPRA-IITJ network.

To start using the tool instantly:

* Fill up the **config.json** file with valid [username, password] combinations.
* `cd` to the repository directory and run `python wgtool.py &` in the command line.

This will add a system tray icon and start the tool in `Auto` mode.

## Configuration

The configuration data is written in `config.json`.

The first object has a list of `username: password` pairs
that are used by the tool for logging in. When the user clicks `Login` from the tray icon menu, it automatically
checks all the mentioned usernames and logs in with the first valid hit.

The second object currently has the `timeout` value only. When the tool is in `Auto` mode, it rechecks if the user
is logged into watchguard portal every `k` seconds, `k` being the timeout value, and logs the user in if not
already logged in. **Default timeout value is 30 seconds**.
This second object can have more configuration options as per the needs.

## Resources Used

`wgtool.py` is the main driving script, and `wutility.py` has all the required definitions.
Some of the primary modules and methods used are:

* `gtk`, `gobject`, `notify` and `appindicator` from `gi.repository`
* `urllib2`
* `requests`
* `json.load`

To run this app on startup, we can write a new small `wgtool.conf` file and put it in /etc/init to hook
into the upstart service that runs services on startup. Then we can also `sudo service wgtool start/stop`.
