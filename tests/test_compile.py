import src.config as config
import src.plotting as ploting

def test_arg_range_config_table():
    configs = config.init_rng()
    ploting.config_table(configs, (1,2))
    ploting.config_table(configs)