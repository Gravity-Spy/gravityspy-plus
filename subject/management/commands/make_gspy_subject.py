from django.core.management.base import BaseCommand, CommandError
from subject.models import GravitySpySubject
from gravityspy_ligo.table.events import Events
from gravityspy_ligo.utils import utils

class Command(BaseCommand):
    help = 'Querying hveto results and product Gravity Spy Plus subjects'
    def add_arguments(self, parser):
        parser.add_argument("--start-time", type=int, required=True)
        parser.add_argument("--end-time", type=int, required=True)

    def handle(self, *args, **options):

        ### Select the parameters of the spectrograms/q_transforms you will be plotting (including all of the different plotting windows your would like
        config = utils.GravitySpyConfigFile(plot_time_ranges=[8.0, 4.0, 1.0])

        ### Get list of GPS times which correspond with a glitch occur in the main channel. This can either be done manually, querying omicron directly, or uses hveto's glitches list for a given day.
        start_time = options['start_time']
        end_time = options['end_time']

        table_of_glitch_times = Events.get_triggers(start=start_time, end=end_time, channel='H1:GDS-CALIB_STRAIN', dqflag=None, algorithm='hveto', verbose=True)

        table_of_glitch_times = table_of_glitch_times[0:2]

        for event_time, round_number in zip(table_of_glitch_times['time'], table_of_glitch_times['hveto_round']):
            breakpoint()
            sub = GravitySpySubject.objects.create_gravityspy_subject(event_time=event_time, ifo="H1", config=config, auxiliary_channel_correlation_algorithm={'hveto':round_number}, number_of_aux_channels_to_show=6)
            breakpoint()
            sub.make_omega_scans(verbose=False, nproc=7)
            sub.save_omega_scans(verbose=False, nproc=7)
            # This method needs to be written
            sub.combine_images_for_subject_upload()
            # no need to upload data to zooniverse until we finalize the way we combine the spectrograms into a single user friendly image
            sub.upload_to_zooniverse(subject_set_id=103434)
