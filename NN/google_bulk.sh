# Used to extract all the images from a Google Image Search 

# go to google search and search for what you want
# press alt+command+I to open developer tools
# in the developer tools select network tab
# in the file types select “img”
# refresh the page
# in the filter box write “images?q=”
# scroll down to the bottom to get as many pictures as you like
# on the “Name” pane right click an image
# expand Copy
# select Copy All as cURL
# open terminal
# cd into your favorite folder
pbpaste | awk '{print substr($0, 1, length($0)-1) ">>" NR ".jpg"}' | bash