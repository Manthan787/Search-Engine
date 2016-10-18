from ..config import RESULT_PATH, ASSESSOR_ID
from os.path import join
from django.utils.encoding import iri_to_uri


class GradesWriter(object):


    def __init__(self, data):
        """
        :param data: a list containing grades for each URL
        :return: Void
        """
        self.data = data


    def write(self, output_file, queryID):
        """
        :param output_file: the name (string) of the file where the grades are to be stored
        :param queryID: ID of the query being assessed
        :return: Void
        """
        print "Writing grades to file!"
        location = join(RESULT_PATH, output_file)
        grade_string = ""
        for grade in self.data:
            grade_string += "{}\t{}\t{}\t{}\n".format(queryID, ASSESSOR_ID, iri_to_uri(grade['url']), grade['grade'])

        f = open(location, 'w')
        f.write(grade_string)
        f.close()

        print "Done writing!"