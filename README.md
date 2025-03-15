# NoCodeWebService

## CrowdWare
Thi app is ment for crowdfunding with CrowdWare 

## Stripe
We install a hook for stripe with the stripe_app.
We need that in order to sell licenses for the FreeBookDesigner and the NoCodeDesigner.

## NoCode
This app is ment to serve the first online course. (not used atm, we temp. switched to Wordpress)




# Backups
mysqldump -u artanidos -h artanidos.mysql.pythonanywhere-services.com --set-gtid-purged=OFF --no-tablespaces --column-statistics=0 'artanidos$nocode'  > nocode-backup.sql