from typing import Dict
from dataclasses import dataclass

from ..utils.plink import run_plink
from ..utils.cache import FileCache


@dataclass
class QCArgs:
    sample: Dict[str, str]
    variant: Dict[str, str]


class QC:
    def __init__(self, qc_config: Dict) -> None:
        self.qc_config = qc_config
    
    def fit_transform(self, cache: FileCache) -> None:
        # Create a new output path for QC-processed data
        qc_path = str(cache.pfile_path()) + "_qc"

        run_plink(
            args_list=[
                '--pfile', str(cache.pfile_path()),
                '--make-pgen'
            ],
            args_dict={
                '--out': qc_path,
                '--set-missing-var-ids': '@:#:$r:$a',
                **self.qc_config
            }
        )

        # ✅ VERY IMPORTANT: update cache to point to QC output
        cache._pfile_path = qc_path
    
    def transform(self, source_path: str, dest_path: str) -> None:
        run_plink(args_list=['--make-pgen', '--pfile', str(source_path)],
                  args_dict={**{'--out': str(dest_path),
                                '--set-missing-var-ids': '@:#'},
                             **self.qc_config})
