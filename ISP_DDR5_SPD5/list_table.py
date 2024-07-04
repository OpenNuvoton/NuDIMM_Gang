dimm_type = [
"Reserved",
"RDIMM",
"UDIMM",
"SODIMM",
"LRDIMM",
"CUDIMM",
"CSODIMM",
"MRDIMM",
"CAMM2",
"Reserved",
"DDIMM",
"Solder down"
]

pmic = [
"PMIC5000",
"PMIC5010",
"PMIC5100",
"PMIC5020",
"PMIC5120",
"PMIC5200",
"PMIC5030"
]

ts5 = [
"TS5111",
"TS5110",
"TS5211",
"TS5210"
]

module_speed = [
[3200,0x1E,0x00,0x00,0x00,0x00],
[3200,0x1A,0x00,0x00,0x00,0x00],
[3200,0x1A,0x00,0x00,0x00,0x00],
[3200,0x12,0x00,0x00,0x00,0x00],
[3600,0x7E,0x00,0x00,0x00,0x00],
[3600,0x7A,0x00,0x00,0x00,0x00],
[3600,0x72,0x00,0x00,0x00,0x00],
[3600,0x52,0x00,0x00,0x00,0x00],
[4000,0x7E,0x01,0x00,0x00,0x00],
[4000,0x7A,0x01,0x00,0x00,0x00],
[4000,0x7A,0x01,0x00,0x00,0x00],
[4000,0x52,0x01,0x00,0x00,0x00],
[4400,0x7E,0x05,0x00,0x00,0x00],
[4400,0x7A,0x05,0x00,0x00,0x00],
[4400,0x72,0x05,0x00,0x00,0x00],
[4400,0x52,0x05,0x00,0x00,0x00],
[4800,0xFE,0x0D,0x00,0x00,0x00],
[4800,0x7A,0x0D,0x00,0x00,0x00],
[4800,0x72,0x0D,0x00,0x00,0x00],
[4800,0x52,0x0D,0x00,0x00,0x00],
[5200,0x7E,0x2F,0x00,0x00,0x00],
[5200,0x7A,0x2D,0x00,0x00,0x00],
[5200,0x7A,0x2D,0x00,0x00,0x00],
[5200,0x52,0x2D,0x00,0x00,0x00],
[5600,0x7E,0xAF,0x00,0x00,0x00],
[5600,0x7A,0xAD,0x00,0x00,0x00],
[5600,0x72,0xAD,0x00,0x00,0x00],
[5600,0x52,0xAD,0x00,0x00,0x00],
[6000,0xFE,0xEF,0x02,0x00,0x00],
[6000,0x7A,0xED,0x02,0x00,0x00],
[6000,0x7A,0xED,0x02,0x00,0x00],
[6000,0x52,0xAD,0x02,0x00,0x00],
[6400,0x7E,0xEF,0x07,0x00,0x00],
[6400,0x7A,0xED,0x07,0x00,0x00],
[6400,0x7A,0xED,0x07,0x00,0x00],
[6400,0x52,0xAD,0x06,0x00,0x00],
[6800,0xFE,0xEF,0xF7,0x00,0x00],
[6800,0x7A,0xED,0x17,0x00,0x00],
[6800,0x72,0xAD,0x16,0x00,0x00],
[6800,0x52,0xAD,0x16,0x00,0x00],
[7200,0x7E,0xEF,0x5F,0x00,0x00],
[7200,0x7A,0xED,0x5F,0x00,0x00],
[7200,0x7A,0xAD,0x5F,0x00,0x00],
[7200,0x52,0xAD,0x56,0x00,0x00],
[7600,0x7E,0xED,0x7F,0x01,0x00],
[7600,0x7A,0xED,0x7F,0x01,0x00],
[7600,0x72,0xAD,0x76,0x01,0x00],
[7600,0x52,0xAD,0x56,0x01,0x00],
[8000,0xFE,0xEF,0x7F,0x03,0x00],
[8000,0x7A,0xED,0x7F,0x03,0x00],
[8000,0x7A,0xED,0x7F,0x03,0x00],
[8000,0x52,0xAD,0x56,0x03,0x00],
[8400,0x7E,0xEF,0x7F,0x0B,0x00],
[8400,0x7A,0xED,0x7F,0x0B,0x00],
[8400,0x7A,0xAD,0x77,0x0B,0x00],
[8400,0x52,0xAD,0x56,0x0B,0x00],
[8800,0xFE,0xEF,0x7F,0x2F,0x00],
[8800,0x7A,0xED,0x7F,0x2F,0x00],
[8800,0x72,0xAD,0x56,0x2F,0x00],
[8800,0x52,0xAD,0x56,0x2B,0x00]
]