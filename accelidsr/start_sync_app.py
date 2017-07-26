# import os, sys, inspect
#
# cmd_folder = os.path.realpath(os.path.abspath(os.path.split(inspect.getfile( inspect.currentframe() ))[0]))
# if cmd_folder not in sys.path:
#    print 'lalall'
#    sys.path.insert(0, cmd_folder)
#
# cmd_subfolder = os.path.realpath(os.path.abspath(os.path.join(os.path.split(inspect.getfile(inspect.currentframe() ))[0], "accel_idsr_sync")))
# if cmd_subfolder not in sys.path:
#    sys.path.insert(0, cmd_subfolder)
#
# import run.Run
# runner = Run()
# # runner.start()


from accel_idsr_sync.run import Run

runner = Run()
runner.start()