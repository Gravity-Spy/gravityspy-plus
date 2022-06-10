from django.core.management.base import BaseCommand, CommandError
import panoptes_client

class Command(BaseCommand):
    help = 'Querying the Gravity Spy Plus zooniverse project for classifications'
    def add_arguments(self, parser):
        parser.add_argument("--project-id", default='9979')
        parser.add_argument("--last-classification-id", type=int, default=None)

    def handle(self, *args, **options):
        if options['last_classification_id'] is not None:
            all_classifications = panoptes_client.Classification.where(project_id=options['project_id'], scope='project', last_id='{0}'.format(options['last_classification_id']), page_size='100')
        else:
            all_classifications = panoptes_client.Classification.where(project_id=options['project_id'], scope='project', page_size='100')

        list_of_classification_dictionaries = []
        # Loop until no more classifications
        for iN in range(0,all_classifications.object_count):
            try:
                classification = all_classifications.next()
                list_of_classification_dictionaries.append(classification.raw)
            except:
                break

        for classification in list_of_classification_dictionaries:
            if classification['links']['workflow'] == '21793':
                print("id is {0}".format(classification['id']))
                print("annotation is {0}".format(classification['annotations']))
                print("workflow is {0}".format(classification['links']['workflow']))
                print("user is {0}".format(classification['links']['user']))
                print("subject is {0}".format(classification['links']['subjects'][0]))
