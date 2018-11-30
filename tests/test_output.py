import os
from nose2.tools import such
from sideeye import calculate_all_measures, parser

with such.A('Output Generator') as it:
    @it.has_setup
    def setup():
        dirname = os.path.dirname(os.path.realpath(__file__))
        it.experiment = parser.experiment.parse(
            os.path.join(dirname, 'testdata/timdrop.DA1'),
            os.path.join(dirname, 'testdata/timdropDA1.cnt')
        )

    @it.should('generate output in long format.')
    def test_long_output():
        output = calculate_all_measures([it.experiment])
        it.assertEqual(
            output.split('\n')[0],
            '''experiment_name,trial_id,trial_total_time,item_id,item_condition,region_number,\
skip,first_pass_regressions_out,first_pass_regressions_in,first_fixation_duration,\
single_fixation_duration,first_pass,go_past,total_time,right_bounded_time,reread_time,\
second_pass,spillover_time,refixation_time,landing_position,launch_site,\
first_pass_fixation_count,go_back_time_region,go_back_time_char,location_first_regression,\
latency_first_regression,fixation_count,percent_regressions,average_forward_saccade,\
average_backward_saccade'''
        )

it.createTests(globals())
