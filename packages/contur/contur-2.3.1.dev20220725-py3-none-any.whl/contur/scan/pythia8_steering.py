import os
import contur
import contur.config.config as cfg

def gen_pythia8_commands(directory_name, run_info, num_events, beam):
    """
    Generate the (shell) commands needed to run the pythia 8 standalone event generator.

    :param directory_name: name of the directory (without any path) in the which batch job will run (usual 4 integers eg 0123
    :param run_info: the local runinfo directory name 
    :param num_events: number of events to generate
    :param beam: the collider beam being run. (should be in contur.data.static_db.known_beams, though this is not currently checked.)


    """
    	
	
    run_card_name = cfg.mceg_template
    pythia8_commands = ""



    pythia8_commands += ('pythia8-main93 -c {} -o  LHC-{}{} -n {}\n').format(run_card_name,cfg.tag,directory_name,num_events)
 


    return pythia8_commands


