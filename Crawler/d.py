from threading import Thread, local


storage = local()

threads = []

def p():
	storage.val = "This is me!"
	print "I'm executing!"


for i in range(0, 2):
	t = Thread(target=p)
	threads.append(t)
	t.setDaemon(True)
	t.start()


[t.join() for t in threads]
print getattr(local, 'val', None)