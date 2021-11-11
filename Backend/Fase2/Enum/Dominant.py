from Enum.typeExpression import typeExpression

Dominant = [
                #STRING                     INTEGER                     FLOAT                        BOOL                       CHAR                        OBJECT
    #STRING
    [   
                typeExpression.STRING,      typeExpression.STRING,      typeExpression.STRING,       typeExpression.ERROR,       typeExpression.ERROR,      typeExpression.STRING
    ],
    #INTEGER
    [
                typeExpression.STRING,      typeExpression.INTEGER,     typeExpression.FLOAT,       typeExpression.ERROR,       typeExpression.ERROR,       typeExpression.INTEGER
    ],
    #FLOAT
    [
                typeExpression.STRING,      typeExpression.FLOAT,       typeExpression.FLOAT,       typeExpression.ERROR,       typeExpression.ERROR,       typeExpression.FLOAT
    ],
    #BOOL
    [
                typeExpression.ERROR,       typeExpression.ERROR,       typeExpression.ERROR,       typeExpression.BOOL,        typeExpression.ERROR,       typeExpression.BOOL
    ],
    #CHAR
    [
                typeExpression.ERROR,       typeExpression.ERROR,       typeExpression.ERROR,       typeExpression.ERROR,        typeExpression.CHAR,       typeExpression.CHAR
    ],
    #OBJECT
    [
                typeExpression.STRING,       typeExpression.INTEGER,       typeExpression.FLOAT,       typeExpression.BOOL,        typeExpression.CHAR,       typeExpression.ERROR
    ]
]