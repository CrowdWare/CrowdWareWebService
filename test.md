  curl -X POST https://artanidos.pythonanywhere.com/crowdware/items \
  -H "Content-Type: application/json" \
  -d '{
    "type": "book",
    "name": "CrowdFund to Take the System Down",
    "description": "**CrowdFund to Take the System Down**\nWie wir die alte Wirtschaft hinter uns lassen und eine neue Welt erschaffen – ohne Schulden, ohne Abhängigkeit, ohne Ausbeutung. Das System will, dass du glaubst, es gäbe keinen Ausweg. Doch das ist eine Lüge.\nDieses Buch zeigt dir, wie du dich aus der finanziellen und wirtschaftlichen Abhängigkeit befreist.",
    "locale": "de",
    "url": "book:https://adamartananda.github.io/CrowdFundToTakeTheSystemDown",
    "pictureurl": "https://raw.githubusercontent.com/AdamArtAnanda/CrowdFundToTakeTheSystemDown/main/images/cover-de.png",
    "account": "1c0bf2f6-0ba3-4183-9847-f98c947fcad2"
  }'
