cd static
yarn install
mv node_modules/@bower_components vendors/
rm -R node_modules
sass assets/scss/style.scss assets/css/style.css