from django.core.management.base import BaseCommand, CommandError
from subject.models import GravitySpySubject
from gravityspy_ligo.table.events import Events
from gravityspy_ligo.utils import utils

class Command(BaseCommand):
    help = 'Querying hveto results and product Gravity Spy Plus subjects'
    def add_arguments(self, parser):
        parser.add_argument("--start-time", type=float)
        parser.add_argument("--end-time", type=float)
        parser.add_argument("--event-time", type=float, default=None)
        parser.add_argument("--ifo")
        parser.add_argument("--manual-list-of-auxiliary-channel-names", nargs="+")

    def handle(self, *args, **options):

        ### Select the parameters of the spectrograms/q_transforms you will be plotting (including all of the different plotting windows your would like
        config = utils.GravitySpyConfigFile(plot_time_ranges=[8.0, 4.0, 1.0])

        # If we have a specific
        if options['event_time'] is not None:

            # initialize the Django model
            sub = GravitySpySubject.objects.create_gravityspy_subject(event_time=options['event_time'], ifo=options['ifo'], config=config, manual_list_of_auxiliary_channel_names=options['manual_list_of_auxiliary_channel_names'])

            # Make the spectrograms/omega scans for each data stream
            GravitySpySubject.objects.make_omega_scans(verbose=False, nproc=1)

            # Save the spectrograms as PNGs with specific settings                
            GravitySpySubject.objects.save_omega_scans(verbose=False, nproc=1)

            # Combine the individual spectrogram images into images with 1 columns and 4 rows
            GravitySpySubject.objects.combine_images_for_subject_upload()

            # upload the subject to zooniverse 
            GravitySpySubject.objects.upload_to_zooniverse(subject_set_id=103434)

            # save out subject
            sub.save()
        else:
            ### Get list of GPS times which correspond with a glitch occur in the main channel. This can either be done manually, querying omicron directly, or uses hveto's glitches list for a given day.
            start_time = options['start_time']
            end_time = options['end_time']

            table_of_glitch_times = Events.get_triggers(start=start_time, end=end_time, channel='{0}:GDS-CALIB_STRAIN'.format(options['ifo']), dqflag=None, algorithm='hveto', verbose=True)

            table_of_glitch_times = Events.from_pandas(table_of_glitch_times.to_pandas().groupby("hveto_round").sample(n=9))

            for event_time, round_number in zip(table_of_glitch_times['time'], table_of_glitch_times['hveto_round']):

                # initialize the Django model
                sub = GravitySpySubject.objects.create_gravityspy_subject(event_time=event_time, ifo=options['ifo'], config=config, auxiliary_channel_correlation_algorithm={'hveto':round_number}, number_of_aux_channels_to_show=9)

                # Make the spectrograms/omega scans for each data stream
                GravitySpySubject.objects.make_omega_scans(verbose=False, nproc=7)

                # Save the spectrograms as PNGs with specific settings  
                GravitySpySubject.objects.save_omega_scans(verbose=False, nproc=7)

                # Combine the individual spectrogram images into images with 1 columns and 4 rows
                GravitySpySubject.objects.combine_images_for_subject_upload()

                # upload the subject to zooniverse 
                GravitySpySubject.objects.upload_to_zooniverse(subject_set_id=103434)

                breakpoint()

                # save out subject
                sub.save()
