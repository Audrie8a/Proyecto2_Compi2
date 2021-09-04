from Enum.typeExpression import typeExpression

Dominant = [
                #STRING                     INTEGER                     FLOAT                        BOOL
    #STRING
    [   
                typeExpression.STRING,      typeExpression.STRING,      typeExpression.STRING,       typeExpression.ERROR
    ],
    #INTEGER
    [
                typeExpression.STRING,      typeExpression.INTEGER,     typeExpression.FLOAT,       typeExpression.ERROR
    ],
    #FLOAT
    [
                typeExpression.STRING,      typeExpression.FLOAT,       typeExpression.FLOAT,       typeExpression.ERROR
    ],
    #BOOL
    [
                typeExpression.ERROR,       typeExpression.ERROR,       typeExpression.ERROR,       typeExpression.BOOL
    ]
]