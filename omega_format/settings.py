from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    # https://pydantic-docs.helpmanual.io/usage/settings/

    ALLOW_MISSING_TL_GROUPS: bool  = True  # allow e.g. weather not to be present
    ALLOW_INCOMPLETE_META_DATA: bool = True
    COMPRESS_HDF5: bool = True
    model_config = SettingsConfigDict(env_prefix='omega_format_', env_file=".env", extra="ignore")

    @property
    def hdf5_compress_args(self):
        if self.COMPRESS_HDF5:
            return dict(compression='gzip', compression_opts=9)
        else:
            return {}

class SettingsGetter:
    def __init__(self, **kwargs):
        self.settings = Settings(**kwargs)

    def set(self, **kwargs):
        for k, v in kwargs.items():
            if v is not None:
                setattr(self.settings, k, v)

    def __call__(self, *args, **kwargs) -> Settings:
        return self.settings


get_settings = SettingsGetter()


class DefaultValues:
    # length, width, height
    # TODO we could use the enum classes to handle this with less if else
    pedestrian = [0.4, 0.53, 1.9]
    bicycle = [1.70, 0.7, 1.9]
    sign = [.1, 1, 1.9]
