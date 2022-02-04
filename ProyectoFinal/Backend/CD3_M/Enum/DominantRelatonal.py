from Enum.typeExpression import typeExpression

DominantRelational = [
                #STRING                     INTEGER                     FLOAT                       BOOL                        CHAR                        OBJECT
    #STRING
    [   
                typeExpression.STRING,      typeExpression.ERROR,       typeExpression.ERROR,       typeExpression.ERROR,       typeExpression.ERROR,       typeExpression.STRING          
    ],
    #INTEGER
    [
                typeExpression.ERROR,      typeExpression.FLOAT,        typeExpression.FLOAT,       typeExpression.INTEGER,     typeExpression.ERROR,       typeExpression.FLOAT
    ],
    #FLOAT
    [
                typeExpression.ERROR,      typeExpression.FLOAT,        typeExpression.FLOAT,       typeExpression.INTEGER,     typeExpression.ERROR,       typeExpression.FLOAT
    ],
    #BOOL
    [
                typeExpression.ERROR,      typeExpression.INTEGER,      typeExpression.INTEGER,     typeExpression.BOOL,        typeExpression.ERROR,       typeExpression.BOOL
    ],
    #CHAR
    [
                typeExpression.ERROR,      typeExpression.ERROR,        typeExpression.ERROR,       typeExpression.ERROR,       typeExpression.CHAR,        typeExpression.CHAR
    ],
    #OBJECT
    [
                typeExpression.STRING,      typeExpression.FLOAT,       typeExpression.FLOAT,       typeExpression.BOOL,        typeExpression.CHAR,        typeExpression.ERROR
    ],
]