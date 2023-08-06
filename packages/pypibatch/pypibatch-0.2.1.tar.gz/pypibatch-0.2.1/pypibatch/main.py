import os
import sys
from datetime import datetime
from types import TracebackType
from typing import List, Tuple, Type, Union

import clr
import pandas as pd

PISDKHOME = os.getenv("PISDKHOME")
sys.path.append(PISDKHOME)

clr.AddReference("OSIsoft.PISDK")

from PISDK import PISDK, PISubBatch, PIUnitBatch



class PiBatchError(Exception):
    def __init__(self, err: str) -> None:
        self.err = err

    def __str__(self) -> str:
        return self.err

class NoBatchesFound(Exception):
    def __init__(self) -> None:
        pass

    def __str__(self) -> str:
        return "Query returned 0 results"


class PiBatch:
    """
    Class for querying PIBatch data via the PISDK
    
    Parameters
    - server (str): the name of the PIServer to connect to
    """

    def __init__(self, server: str) -> None:
        self._server = server

    def connect(self) -> None:
        """Connect to PI Batch DB"""
        if not hasattr(self, '_db'):
            try:
                db = PISDK().Servers[self._server].PIModuleDB
            except BaseException as err:
                raise PiBatchError(repr(err))
            else:
                setattr(self, '_db', db)

    def close(self) -> None:
        """Close PI Batch DB connection"""
        if hasattr(self, '_db'):
            if self._db.Server.Connected:
                self._db.Server.Close()
            del self._db

    def search(
        self,
        unit_id: str,
        start_time: Union[datetime, str] = "-100d",
        end_time: Union[datetime, str] = "*",
        batch_id: Union[List[str], str] = "*",
        product: Union[List[str], str] = "*",
        procedure: Union[List[str], str] = "*",
        sub_batches: Union[List[str], str] = "*"
    ) -> Tuple[pd.DataFrame, pd.DataFrame]:
        """
        Query batches for a given unit_id

        Parameters
        - unit_id (str): Wildcard string of a PIModule name to match
        - start_time (Union[datetime, str]): The search start time.
        datetime.datetime objects are converted to ISOFormat strings
        - end_time (Union[datetime, str]): The search end time.
        datetime.datetime objects are converted to ISOFormat strings.
        Defaults to "*"
        - batch_id (Union[List[str], str]): Wildcard string of BatchID to match.
        List instances are concatenated to a single string separated by commas
        ",". Defaults to "*"
        - product (Union[List[str], str]): Wildcard string of Product to match.
        List instances are concatenated to a single string separated by commas
        ",". Defaults to "*"
        - procedure (Union[List[str], str]): Wildcard string of Procedure to match.
        List instances are concatenated to a single string separated by commas
        ",". Defaults to "*"
        - sub_batches (Union[List[str], str]): Wildcard string of SubBatch to match.
        List instances are concatenated to a single string separated by commas
        ",". Defaults to "*"

        
        Returns
        - UnitBatches (pd.DataFrame): DataFrame of unit batches with schema
            "BatchID": str
            "Product": str
            "Name": str
            "StartTime": str
            "EndTime": str
            "Procedure": str
            "UniqueID": str
            "SubBatchCount": int
        - SubBatches (pd.DataFrame): Dataframe of sub batches with schema
            "ParentID": str (PIUnitBatch.UniqueID)
            "Name": str
            "StartTime": str
            "EndTime": str
            "UniqueID": str (PISubBatch.UniqueID)

        Raises
        - PIBatchError: An error occurred in connecting to server or during
        query
        - NoBatchesFound: Query returned no results
        
        """
        if not hasattr(self, '_db'):
            raise RuntimeError("Not connected")
        start_time, end_time, batch_id, product, procedure, sub_batches = self._prep_search_criteria(
            start_time,
            end_time,
            batch_id,
            product,
            procedure,
            sub_batches
        )
        try:
            unit_batches_raw = [
                PIUnitBatch(batch) for batch in self._db.PIUnitBatchSearch(
                    start_time, end_time, unit_id, batch_id, product, procedure, sub_batches
                )
            ]
        except BaseException as err:
            raise PiBatchError(repr(err))
        if not unit_batches_raw:
            raise NoBatchesFound()
        sub_batches_raw = {
            unit_batch.UniqueID: unit_batch.PISubBatches for unit_batch in unit_batches_raw
        }
        # parse unit batches and sub batches to dataframes
        now = datetime.now().strftime("%m/%d/%Y %H:%M:%S %p")
        unit_batch_info = self._parse_unit_batches(unit_batches_raw, now)
        sub_batch_info = self._parse_sub_batches(sub_batches_raw, now)
        return unit_batch_info, sub_batch_info

    def _prep_search_criteria(
        self,
        start_time: Union[datetime, str],
        end_time: Union[datetime, str],
        batch_id: Union[List[str], str],
        product: Union[List[str], str],
        procedure: Union[List[str], str],
        sub_batches: Union[List[str], str]
    ) -> Tuple[str, str, str, str, str, str]:

        start_time = start_time.isoformat() if isinstance(start_time, datetime) else start_time
        end_time = end_time.isoformat() if isinstance(end_time, datetime) else end_time
        batch_id = ','.join(batch_id) if isinstance(batch_id, list) else batch_id
        product = ','.join(product) if isinstance(product, list) else product
        procedure = ','.join(procedure) if isinstance(procedure, list) else procedure
        sub_batches = ','.join(sub_batches) if isinstance(sub_batches, list) else sub_batches
        return start_time, end_time, batch_id, product, procedure, sub_batches

    def _parse_unit_batches(self, unit_batches_raw: list, now: str) -> pd.DataFrame:
        
        batch_ids = [unit_batch.BatchID for unit_batch in unit_batches_raw]
        products = [unit_batch.Product for unit_batch in unit_batches_raw]
        unit_names = [unit_batch.PIUnit.Name for unit_batch in unit_batches_raw]
        start_times = [unit_batch.StartTime.LocalDate.ToString() for unit_batch in unit_batches_raw]
        end_times = []
        procedure_names = [unit_batch.ProcedureName for unit_batch in unit_batches_raw]
        unique_ids = [unit_batch.UniqueID for unit_batch in unit_batches_raw]
        sub_batch_counts = [unit_batch.PISubBatches.Count for unit_batch in unit_batches_raw]
        for unit_batch in unit_batches_raw:
            try:
                end_times.append(unit_batch.EndTime.LocalDate.ToString())
            except AttributeError:
                end_times.append(now)
        parsed = {
            "BatchID": batch_ids,
            "Product": products,
            "Name": unit_names,
            "StartTime": start_times,
            "EndTime": end_times,
            "Procedure": procedure_names,
            "UniqueID": unique_ids,
            "SubBatchCount": sub_batch_counts
        }
        return pd.DataFrame.from_dict(parsed)
    
    def _parse_sub_batches(self, sub_batches_raw: dict, now: str) -> pd.DataFrame:
        
        parent_ids = []
        names = []
        start_times = []
        end_times = []
        unique_ids = []
        for parent_id, sub_batch in sub_batches_raw.items():
            unit_sub_batches = [PISubBatch(unit_sub_batch) for unit_sub_batch in sub_batch]
            for unit_sub_batch in unit_sub_batches:
                parent_ids.append(parent_id)
                names.append(unit_sub_batch.Name)
                start_times.append(unit_sub_batch.StartTime.LocalDate.ToString())
                try:
                    end_times.append(unit_sub_batch.EndTime.LocalDate.ToString())
                except AttributeError:
                    end_times.append(now)
                unique_ids.append(unit_sub_batch.UniqueID)
        parsed = {
            "ParentID": parent_ids,
            "Name": names,
            "StartTime": start_times,
            "EndTime": end_times,
            "UniqueID": unique_ids
        }
        return pd.DataFrame.from_dict(parsed)

    def __enter__(self) -> "PiBatch":
        return self

    def __exit__(
        self,
        exc_type: Type[BaseException] = None,
        exc_value: BaseException = None,
        traceback: TracebackType = None,
    ) -> None:
        self.close()
        
