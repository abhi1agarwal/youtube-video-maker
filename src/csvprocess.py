import csv

from src.yvm import VideoMaker


class CSVProcess:
    def __init__(self, file_name, output_file_name):
        self.file_name = file_name
        self.output_file_name = output_file_name
        self.field_names = ['stuff', 'prefix', 'keywords', 'is_done', 'suffix']

    def process(self):
        with open(self.file_name) as csv_input_file:
            with open(self.output_file_name, 'x') as csv_output_file:
                csv_reader_input = csv.DictReader(csv_input_file)
                csv_writer_output = csv.DictWriter(csv_output_file, fieldnames=self.field_names)
                csv_writer_output.writeheader()
                for row in csv_reader_input:
                    if row['is_done'] == 'yes':
                        continue
                    out_row = row.copy()
                    video_maker = VideoMaker(row['stuff'], prefix=row['prefix'], suffix=row['suffix'],
                                             suggested_keywords=row['keywords'])
                    try:
                        video_maker.make_video()
                        video_maker.upload_video()
                    except Exception as ex:
                        out_row['is_done'] = "no_failed"
                        print("[**] Generation for {0} failed {1}".format(row, str(ex)))

                    if video_maker.is_video_made and video_maker.is_video_uploaded:
                        out_row['is_done'] = 'yes'
                    else:
                        out_row['is_done'] = 'no_failed'
                        # out_row['is_done'] = 'yes'
                    print("[**] {0} input -> output {1}".format(str(row), str(out_row)))
                    csv_writer_output.writerow(out_row)



if __name__ == '__main__':
    processor = CSVProcess("../video_detail.csv", "../detail_response.csv")
    processor.process()
