# Hearthstone Card Viewer

This a basic web application for viewing a very specific set of cards from the game Hearthstone.


## Warning: Not suitable for production

### Instructions
* `docker build -t cardviewer:latest .`
* `docker run --net=host -P -e BLIZZARD_ACCESS_TOKEN=${ACCESS_TOKEN_FROM_SECRET_MANAGEMENT} cardviewer:latest`
* Load http://127.0.0.1:8000 in your browser


### Assumptions made

* Port 8000 is open
* host networking works
* If a card's set id isn't found in the metadata, "Core" is returned. 
* Sort direction for card ids is ascending.

