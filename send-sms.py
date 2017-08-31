from twilio.rest import Client

# Your Account SID from twilio.com/console
account_sid = "ACaa3b6152eb04409b07fa17010874fd2c"
# Your Auth Token from twilio.com/console
auth_token  = "e972e191d30f27190c49fda19e3d22a7"

client = Client(account_sid, auth_token)

message = client.messages.create(
    to="+14158285205", 
    from_="+14157024024",
    body="Hello from Python!")

print(message.sid)