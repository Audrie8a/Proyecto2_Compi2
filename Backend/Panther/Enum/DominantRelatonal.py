from Enum.typeExpression import typeExpression

DominantRelational = [
                #STRING                     INTEGER                     FLOAT                       BOOL
    #STRING
    [   
                typeExpression.STRING,      typeExpression.ERROR,      typeExpression.ERROR,        typeExpression.ERROR          
    ],
    #INTEGER
    [
                typeExpression.ERROR,      typeExpression.FLOAT,     typeExpression.FLOAT,        typeExpression.INTEGER
    ],
    #FLOAT
    [
                typeExpression.ERROR,      typeExpression.FLOAT,       typeExpression.FLOAT,      typeExpression.INTEGER
    ],
    #BOOL
    [
                typeExpression.ERROR,      typeExpression.INTEGER,       typeExpression.INTEGER,      typeExpression.BOOL
    ]
]