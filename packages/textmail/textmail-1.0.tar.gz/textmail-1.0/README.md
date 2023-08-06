```python
from mailer.TextMessage import TextMessage
from mobile.tmobile import TMobile
from mobile.verizon import Verizon
from mobile.sprint import Sprint
from providers.email_credentials import Credentials
from providers.gmail import Gmail

message = TextMessage(Credentials("john@gmail.com", "[App Password]", Gmail()))
```
##Send email with list of Strings
``` python
message.email(subject="Hello world!", body="This is the message body.", recipients=["dave@gmail.com", "mark@gmail.com", "kyle@yahoo.com"])
```
##Send email with list of Email objects
``` python
message.email(subject="Hello world!", body="This is the message body.", recipients=[Email("dave@gmail.com"), Email("mark@gmail.com"), Email("kyle@yahoo.com")])
```

##Send a text message
```python
message.text(subject="Hello world!", body="This is the message body.", recipients=[ Sprint("0001112233")])
```

##Send to a mix
```python
message.send(subject="Hello world!", body="This is the message body.", recipients=[Email("dave@gmail.com"), Verizon("1234567890"), ATNT("0987654321")])
```
