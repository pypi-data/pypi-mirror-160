import sys


class CacheHandlerError(Exception): pass

class HandlerCache():
    def __int__(self): pass

    @staticmethod
    def addlogTable(fun, currentSql):
        sql_list = str(currentSql).split(" ")
        sqlf=HandlerCache.sqlfield()
        tablelist=[i for i in sql_list if i not in sqlf]
        tables=[i.split('(')[0] for i in tablelist if i.split('(')[0] not in sqlf][0]
        #Ut001-annosSQL.Donos.dosql-execute
        container=sys.modules[str(fun.cla).split(' ')[1].split('.')[0]+'-'+fun.__class__.__module__ + '-' + fun.__class__.__name__]
        logsTable=container['cachePool']['logsTable']
        if tables in logsTable:
            logsTable.append(tables)
    @staticmethod
    def sqlfield():
        sqlFlist = \
            """
            ADD	ALL	ALTER
            ANALYZE	AND	AS
            ASC	ASENSITIVE	BEFORE
            BETWEEN	BIGINT	BINARY
            BLOB	BOTH	BY
            CALL	CASCADE	CASE
            CHANGE	CHAR	CHARACTER
            CHECK	COLLATE	COLUMN
            CONDITION	CONNECTION	CONSTRAINT
            CONTINUE	CONVERT	CREATE
            CROSS	CURRENT_DATE	CURRENT_TIME
            CURRENT_TIMESTAMP	CURRENT_USER	CURSOR
            DATABASE	DATABASES	DAY_HOUR
            DAY_MICROSECOND	DAY_MINUTE	DAY_SECOND
            DEC	DECIMAL	DECLARE
            DEFAULT	DELAYED	DELETE
            DESC	DESCRIBE	DETERMINISTIC
            DISTINCT	DISTINCTROW	DIV
            DOUBLE	DROP	DUAL
            EACH	ELSE	ELSEIF
            ENCLOSED	ESCAPED	EXISTS
            EXIT	EXPLAIN	FALSE
            FETCH	FLOAT	FLOAT4
            FLOAT8	FOR	FORCE
            FOREIGN	FROM	FULLTEXT
            GOTO	GRANT	GROUP
            HAVING	HIGH_PRIORITY	HOUR_MICROSECOND
            HOUR_MINUTE	HOUR_SECOND	IF
            IGNORE	IN	INDEX
            INFILE	INNER	INOUT
            INSENSITIVE	INSERT	INT
            INT1	INT2	INT3
            INT4	INT8	INTEGER
            INTERVAL	INTO	IS
            ITERATE	JOIN	KEY
            KEYS	KILL	LABEL
            LEADING	LEAVE	LEFT
            LIKE	LIMIT	LINEAR
            LINES	LOAD	LOCALTIME
            LOCALTIMESTAMP	LOCK	LONG
            LONGBLOB	LONGTEXT	LOOP
            LOW_PRIORITY	MATCH	MEDIUMBLOB
            MEDIUMINT	MEDIUMTEXT	MIDDLEINT
            MINUTE_MICROSECOND	MINUTE_SECOND	MOD
            MODIFIES	NATURAL	NOT
            NO_WRITE_TO_BINLOG	NULL	NUMERIC
            ON	OPTIMIZE	OPTION
            OPTIONALLY	OR	ORDER
            OUT	OUTER	OUTFILE
            PRECISION	PRIMARY	PROCEDURE
            PURGE	RAID0	RANGE
            READ	READS	REAL
            REFERENCES	REGEXP	RELEASE
            RENAME	REPEAT	REPLACE
            REQUIRE	RESTRICT	RETURN
            REVOKE	RIGHT	RLIKE
            SCHEMA	SCHEMAS	SECOND_MICROSECOND
            SELECT	SENSITIVE	SEPARATOR
            SET	SHOW	SMALLINT
            SPATIAL	SPECIFIC	SQL
            SQLEXCEPTION	SQLSTATE	SQLWARNING
            SQL_BIG_RESULT	SQL_CALC_FOUND_ROWS	SQL_SMALL_RESULT
            SSL	STARTING	STRAIGHT_JOIN
            TABLE	TERMINATED	THEN
            TINYBLOB	TINYINT	TINYTEXT
            TO	TRAILING	TRIGGER
            TRUE	UNDO	UNION
            UNIQUE	UNLOCK	UNSIGNED
            UPDATE	USAGE	USE
            USING	UTC_DATE	UTC_TIME
            UTC_TIMESTAMP	VALUES	VARBINARY
            VARCHAR	VARCHARACTER	VARYING
            WHEN	WHERE	WHILE
            WITH	WRITE	X509
            XOR	YEAR_MONTH	ZEROFILL
            """
        sqlFlist=str(sqlFlist).replace('\n', '').replace(' ','\t')
        sqlFlist="\t".join(sqlFlist.lower().split()).split('\t')
        return sqlFlist



class CacheHandler():
    def __init__(self, *args, **kwargs):
        self.id_cursor = 0

    def __call__(self, fun, *args, **kwargs):
        fun = self.forward
        return fun

    def result(self) -> any:
        pass

    def forward(self, fun, currentSql) -> None:
        return getattr(self, fun.sqlType)(fun, currentSql)

    def insert(self, fun, currentSql) -> any:
        result = fun.execSql(fun, currentSql)
        if result >0:
            HandlerCache.addlogTable(fun, currentSql)
        return result

    def update(self, fun, currentSql) -> any:
        result = fun.execSql(fun, currentSql)
        if result >0:
            HandlerCache.addlogTable(fun, currentSql)
        return result

    def delete(self, fun, currentSql) -> any:
        result = fun.execSql(fun, currentSql)
        if result >0:
            HandlerCache.addlogTable(fun, currentSql)
        return result

    def other(self, fun, currentSql) -> any:
        self.select(fun, currentSql)

    def select(self, fun, currentSql) -> result:
        container=sys.modules[str(fun.cla).split(' ')[1].split('.')[0]+'-'+fun.__class__.__module__ + '-' + fun.__class__.__name__]
        logsTable = container['cachePool']['logsTable']
        if len(logsTable)>0 and len(fun.cache)>0:
            tmp=[i[1] for i in fun.physicsTable]
            for i in range(0,len(tmp)):
                for j in logsTable:
                    if j in tmp[i]:
                        logsTable.remove(j)
                        del fun.cache[fun.physicsTable[i][2]]
                        del fun.physicsTable[i]
                        break

        if fun.accessNot >= fun.cacheSize:
            fun.accessNot = 9
        if fun.id_cursor >= fun.cacheSize:
            fun.id_cursor = 0
        cacheCur = None
        for i in range(len(fun.physicsTable)):
            if currentSql in fun.physicsTable[i]:
                cacheCur = i
        if fun.cacheBit == 0:
            data = fun.execSql(fun, currentSql)
            fun.cache[fun.cacheBit] = data
            fun.physicsTable.append([fun.cacheBit, currentSql, self.id_cursor, fun.accessNot])

            fun.cacheBit += 1
            fun.accessNot += 1
            fun.id_cursor += 1
            return data

        if fun.cacheBit > 0 and fun.cacheBit < fun.cacheSize:
            if cacheCur != None:
                fun.access = cacheCur
                fun.physicsTable[cacheCur][3] = fun.accessNot
                for i in range(fun.accessNot + 1, len(fun.physicsTable)):
                    fun.physicsTable[i][3] = fun.physicsTable[i][3] - 1
                    fun.accessNot += 1
                return fun.cache[fun.physicsTable[cacheCur][2]]
            data = fun.execSql(fun, currentSql)
            fun.cache[fun.cacheBit] = data
            fun.physicsTable.append([fun.cacheBit, currentSql, fun.id_cursor, fun.accessNot])
            fun.cacheBit += 1
            fun.accessNot += 1
            fun.id_cursor += 1
            return data
        if fun.cacheBit > 0 and fun.cacheBit == fun.cacheSize:
            if cacheCur != None:
                fun.access = cacheCur
                fun.physicsTable[cacheCur][3] = fun.accessNot
                for i in range(fun.accessNot + 1, len(fun.physicsTable)):
                    fun.physicsTable[i][3] = fun.physicsTable[i][3] - 1
                fun.accessNot += 1
                # print(fun.id_cursor, cacheCur)
                if fun.id_cursor != cacheCur:
                    fun.logicTable.append(cacheCur)
                if fun.id_cursor == cacheCur:
                    fun.id_cursor += 1

                return fun.cache[fun.physicsTable[cacheCur][2]]

            del fun.physicsTable[0]
            for i in range(0, len(fun.physicsTable)):
                fun.physicsTable[i][3] = fun.physicsTable[i][3] - 1
            if len(fun.logicTable) > 0 and fun.id_cursor in fun.logicTable:
                fun.logicTable.remove(fun.id_cursor)
                fun.id_cursor += 1
            data = fun.execSql(fun, currentSql)
            fun.cache[fun.id_cursor] = data
            fun.physicsTable.append([fun.cacheBit, currentSql, fun.id_cursor, fun.accessNot])
            fun.id_cursor += 1
            fun.accessNot += 1
            return data
