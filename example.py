import sys, time
from nats.client import NatsClient

NATS_URI = "nats://nats:nats@127.0.0.1:4242"

def main():
    nats = NatsClient()
    conn, error  = nats.connect_nats({
        "uri" : NATS_URI }
    )
    if error: sys.exit(-1)

    i = 200
    while i>1:
        time.sleep(1)
        i -= 1
        def callback_sub(msg, reply):
            nats.publish(reply, "reply for this")
            print  "received {}".format(msg)
        def callback_req(msg):
            print "received {}".format(msg)

        def callback_pub():
            print "publish msg"

        sid = nats.subscribe("python-nats", {}, callback_sub)
        nats.publish("python-nats", "hello-world", "", callback_pub)
        nats.request("python-nats", "hello-world", {}, callback_req)
        nats.unsubscribe(sid)
    
if __name__ == '__main__':
    main()
