# PyPIBatch

*A simple OSI PI Batch client for python*

**pypibatch relies on the PI SDK for connecting to PI Batch. See *Configuration* below for ensuring proper setup**

## Installation

`pip install pypibatch`

## Usage

```python
from pypibatch import NoBatchesFound, PIBatch

pi = PIBatch("PI_SERVER")

try:
    unit_batches, sub_batches = pi.search("UNIT_NAME")
except NoBatchesFound:
    raise
```

## API Reference

*class* *pypibatch*.***PIBatch***(*server*)

Create a connection to the PI server

**Parameters**

> **server** (*str*): PI server to connect to

**Raises**

> **PIBatchError**: Unable to connect to PI server

*method* *PIBatch*.***search***(*unit_id*, *, *start_time="`*-100d`"*, *end_time=`"*"`*, *batch_id=`"*"`*, *product=`"*"`*, *procedure=`"*"`*, *sub_batches=`"*"`*)

Search for PI unit batches that match the criteria

**Parameters**

> **unit_id** (*str*): Wildcard string of a PIModule name to match
>
> **start_time** (*Union[datetime, str]*): The search start time, datetime objects are converted to ISOFormat
>
> **end_time** (*Union[datetime, str]*): The search end time, datetime objects are converted to ISOFormat
>
> **batch_id** (*Union[list[str], str]*): Wildcard string(s) of BatchID to match, list like objects are joined with a ","
>
> **product** (*Union[list[str], str]*): Wildcard string(s) of Product to match, list like objects are joined with a ","
>
> **procedure** (*Union[list[str], str]*): Wildcard string(s) of ProcedureName to match, list like objects are joined with a ","
>
> **sub_batch** (*Union[list[str], str]*): Wildcard string(s) of SubBatch to match, list like objects are joined with a ","

**Returns**

> **UnitBatches** (pandas.DataFrame): A non empty DataFrame containing the unit batches returned from the query.
>
> ***Schema***
>
> - BatchID: str
> - Product: str
> - Name: str
> - StartTime: str
> - EndTime: str
> - Procedure: str
> - UniqueID: str
> - SubBatchCount: int
>
> **SubBatches** (pandas.DataFrame): A DataFrame containing the sub batches of the returned unit batches. DataFrame may be empty.
>
> ***Schema***
>
> - ParentID: str (PIUnitBatch.UniqueID)
> - Name: str
> - StartTime: str
> - EndTime: str
> - UniqueID: str (PISubBatch.UniqueID)

**Raises**

> **NoBatchesFound**: Query returned no unit batches
>
> **PIBatchError**: Error occurred querying PI Server

## Configuration

- You must set the *PISDKHOME* environment variable to the path of PISDK assemblies. This is typically located in ~Program Files\PIPC\pisdk\PublicAssemblies
- You will need [pythonnet](https://github.com/pythonnet/pythonnet) installed in your Python environment. This is a required dependency but is not installed automatically by pypibatch at the moment because the stable release of pythonnet does not install properly on python >= 3.9. You can try installing pythonnet yourself...

`pip install pythonnet`

You may need to install the pre-release version though...

`pip install pythonnet --pre`

## Dependencies

- pandas
- pythonnet