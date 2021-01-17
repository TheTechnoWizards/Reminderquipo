from reminderquipo import app
from reminderquipo.scheduler import scheduler
from multiprocessing import Process

if __name__ == "__main__":
    # scheduler()
    # app.run(debug=True)
    Process(target=app.run, kwargs=dict(debug=True)).start()
    Process(target=scheduler).start()
    

# while True:
#     scheduler()
#     time.sleep(5)