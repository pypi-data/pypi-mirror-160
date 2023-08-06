from enum import Enum


# noinspection SpellCheckingInspection
class AcpOffset(Enum):
	"""3 Members, LSB ... USB"""
	LSB = 0
	NONE = 1
	USB = 2


# noinspection SpellCheckingInspection
class Activity(Enum):
	"""2 Members, ACTive ... INACtive"""
	ACTive = 0
	INACtive = 1


# noinspection SpellCheckingInspection
class Allow(Enum):
	"""2 Members, ALLowed ... NA"""
	ALLowed = 0
	NA = 1


# noinspection SpellCheckingInspection
class AnalogDigital(Enum):
	"""2 Members, ANALog ... DIGital"""
	ANALog = 0
	DIGital = 1


# noinspection SpellCheckingInspection
class ArbSamplesRange(Enum):
	"""2 Members, FULL ... SUB"""
	FULL = 0
	SUB = 1


# noinspection SpellCheckingInspection
class ArmedState(Enum):
	"""3 Members, ARMed ... TRIGgered"""
	ARMed = 0
	OFF = 1
	TRIGgered = 2


# noinspection SpellCheckingInspection
class AttenuationPort(Enum):
	"""2 Members, LOAD ... SOURce"""
	LOAD = 0
	SOURce = 1


# noinspection SpellCheckingInspection
class AudioConnector(Enum):
	"""2 Members, AF1O ... AF2O"""
	AF1O = 0
	AF2O = 1


# noinspection SpellCheckingInspection
class AudioSource(Enum):
	"""6 Members, DEM ... VOIP"""
	DEM = 0
	DEML = 1
	DEMR = 2
	NONE = 3
	UGEN = 4
	VOIP = 5


# noinspection SpellCheckingInspection
class AveragingMode(Enum):
	"""2 Members, LINear ... LOGarithmic"""
	LINear = 0
	LOGarithmic = 1


# noinspection SpellCheckingInspection
class BandpassFilter(Enum):
	"""5 Members, F01M ... F8330"""
	F01M = 0
	F05M = 1
	F25K = 2
	F50K = 3
	F8330 = 4


# noinspection SpellCheckingInspection
class BaseScenario(Enum):
	"""12 Members, AUDio ... TXTest"""
	AUDio = 0
	AVIonics = 1
	DEXPert = 2
	DRXTest = 3
	DSPectrum = 4
	DTXTest = 5
	DXTest = 6
	EXPert = 7
	RXTest = 8
	SEQuencer = 9
	SPECtrum = 10
	TXTest = 11


# noinspection SpellCheckingInspection
class BatteryUsage(Enum):
	"""3 Members, NAV ... USED"""
	NAV = 0
	REMovable = 1
	USED = 2


# noinspection SpellCheckingInspection
class BerPeriod(Enum):
	"""2 Members, F36 ... F48"""
	F36 = 0
	F48 = 1


# noinspection SpellCheckingInspection
class ByteOrder(Enum):
	"""2 Members, NORMal ... SWAPped"""
	NORMal = 0
	SWAPped = 1


# noinspection SpellCheckingInspection
class CalibType(Enum):
	"""4 Members, CALibration ... UCORrection"""
	CALibration = 0
	FSCorrection = 1
	OGCal = 2
	UCORrection = 3


# noinspection SpellCheckingInspection
class CatalogFormat(Enum):
	"""2 Members, ALL ... WTIMe"""
	ALL = 0
	WTIMe = 1


# noinspection SpellCheckingInspection
class ChannelModeDmr(Enum):
	"""2 Members, DATA ... VOICe"""
	DATA = 0
	VOICe = 1


# noinspection SpellCheckingInspection
class ChannelModeTetra(Enum):
	"""1 Members, TCH72 ... TCH72"""
	TCH72 = 0


# noinspection SpellCheckingInspection
class ChannelTypeTetra(Enum):
	"""8 Members, CT0 ... CT4"""
	CT0 = 0
	CT1 = 1
	CT2 = 2
	CT21 = 3
	CT22 = 4
	CT24 = 5
	CT3 = 6
	CT4 = 7


# noinspection SpellCheckingInspection
class CircuitryState(Enum):
	"""2 Members, ACTive ... PASSive"""
	ACTive = 0
	PASSive = 1


# noinspection SpellCheckingInspection
class ClockRate(Enum):
	"""10 Members, BPS115200 ... BPS9600"""
	BPS115200 = 0
	BPS1200 = 1
	BPS14400 = 2
	BPS19200 = 3
	BPS2400 = 4
	BPS28800 = 5
	BPS38400 = 6
	BPS4800 = 7
	BPS57600 = 8
	BPS9600 = 9


# noinspection SpellCheckingInspection
class CrestFactor(Enum):
	"""2 Members, LOW ... MAXimum"""
	LOW = 0
	MAXimum = 1


# noinspection SpellCheckingInspection
class DataFormat(Enum):
	"""8 Members, ASCii ... UINTeger"""
	ASCii = 0
	BINary = 1
	HEXadecimal = 2
	INTeger = 3
	OCTal = 4
	PACKed = 5
	REAL = 6
	UINTeger = 7


# noinspection SpellCheckingInspection
class DefaultUnitAngle(Enum):
	"""3 Members, DEG ... RAD"""
	DEG = 0
	GRAD = 1
	RAD = 2


# noinspection SpellCheckingInspection
class DefaultUnitCapacity(Enum):
	"""13 Members, AF ... UF"""
	AF = 0
	EXF = 1
	F = 2
	FF = 3
	GF = 4
	KF = 5
	MF = 6
	MIF = 7
	NF = 8
	PEF = 9
	PF = 10
	TF = 11
	UF = 12


# noinspection SpellCheckingInspection
class DefaultUnitCharge(Enum):
	"""13 Members, AC ... UC"""
	AC = 0
	C = 1
	EXC = 2
	FC = 3
	GC = 4
	KC = 5
	MC = 6
	MIC = 7
	NC = 8
	PC = 9
	PEC = 10
	TC = 11
	UC = 12


# noinspection SpellCheckingInspection
class DefaultUnitConductance(Enum):
	"""13 Members, ASIE ... USIE"""
	ASIE = 0
	EXSie = 1
	FSIE = 2
	GSIE = 3
	KSIE = 4
	MISie = 5
	MSIE = 6
	NSIE = 7
	PESie = 8
	PSIE = 9
	SIE = 10
	TSIE = 11
	USIE = 12


# noinspection SpellCheckingInspection
class DefaultUnitCurrent(Enum):
	"""18 Members, A ... UA"""
	A = 0
	AA = 1
	DBA = 2
	DBMA = 3
	DBNA = 4
	DBPA = 5
	DBUA = 6
	EXA = 7
	FA = 8
	GA = 9
	KA = 10
	MA = 11
	MAA = 12
	NA = 13
	PA = 14
	PEA = 15
	TA = 16
	UA = 17


# noinspection SpellCheckingInspection
class DefaultUnitEnergy(Enum):
	"""13 Members, AJ ... UJ"""
	AJ = 0
	EXJ = 1
	FJ = 2
	GJ = 3
	J = 4
	KJ = 5
	MIJ = 6
	MJ = 7
	NJ = 8
	PEJ = 9
	PJ = 10
	TJ = 11
	UJ = 12


# noinspection SpellCheckingInspection
class DefaultUnitFrequency(Enum):
	"""13 Members, AHZ ... UHZ"""
	AHZ = 0
	EXHZ = 1
	FHZ = 2
	GHZ = 3
	HZ = 4
	KHZ = 5
	MHZ = 6
	MIHZ = 7
	NHZ = 8
	PEHZ = 9
	PHZ = 10
	THZ = 11
	UHZ = 12


# noinspection SpellCheckingInspection
class DefaultUnitFullScale(Enum):
	"""4 Members, DBFS ... PPM"""
	DBFS = 0
	FS = 1
	PCT = 2
	PPM = 3


# noinspection SpellCheckingInspection
class DefaultUnitLenght(Enum):
	"""13 Members, AM ... UM"""
	AM = 0
	EXM = 1
	FM = 2
	GM = 3
	KM = 4
	M = 5
	MAM = 6
	MM = 7
	NM = 8
	PEM = 9
	PM = 10
	TM = 11
	UM = 12


# noinspection SpellCheckingInspection
class DefaultUnitPower(Enum):
	"""19 Members, AW ... W"""
	AW = 0
	DBM = 1
	DBMW = 2
	DBNW = 3
	DBPW = 4
	DBUW = 5
	DBW = 6
	EXW = 7
	FW = 8
	GW = 9
	KW = 10
	MIW = 11
	MW = 12
	NW = 13
	PEW = 14
	PW = 15
	TW = 16
	UW = 17
	W = 18


# noinspection SpellCheckingInspection
class DefaultUnitResistor(Enum):
	"""13 Members, AOHM ... UOHM"""
	AOHM = 0
	EXOHm = 1
	FOHM = 2
	GOHM = 3
	KOHM = 4
	MIOHm = 5
	MOHM = 6
	NOHM = 7
	OHM = 8
	PEOHm = 9
	POHM = 10
	TOHM = 11
	UOHM = 12


# noinspection SpellCheckingInspection
class DefaultUnitTemperature(Enum):
	"""6 Members, C ... KEL"""
	C = 0
	CEL = 1
	F = 2
	FAR = 3
	K = 4
	KEL = 5


# noinspection SpellCheckingInspection
class DefaultUnitTime(Enum):
	"""18 Members, AS ... US"""
	AS = 0
	EXS = 1
	FS = 2
	GS = 3
	H = 4
	HOUR = 5
	KS = 6
	M = 7
	MAS = 8
	MIN = 9
	MS = 10
	NS = 11
	PES = 12
	PS = 13
	S = 14
	SEC = 15
	TS = 16
	US = 17


# noinspection SpellCheckingInspection
class DefaultUnitVoltage(Enum):
	"""18 Members, AV ... V"""
	AV = 0
	DBMV = 1
	DBNV = 2
	DBPV = 3
	DBUV = 4
	DBV = 5
	EXV = 6
	FV = 7
	GV = 8
	KV = 9
	MAV = 10
	MV = 11
	NV = 12
	PEV = 13
	PV = 14
	TV = 15
	UV = 16
	V = 17


# noinspection SpellCheckingInspection
class DeltaMode(Enum):
	"""3 Members, MEAS ... USER"""
	MEAS = 0
	NONE = 1
	USER = 2


# noinspection SpellCheckingInspection
class Demodulation(Enum):
	"""6 Members, AM ... USB"""
	AM = 0
	FM = 1
	FMSTereo = 2
	LSB = 3
	PM = 4
	USB = 5


# noinspection SpellCheckingInspection
class DemodulationType(Enum):
	"""1 Members, FSK4 ... FSK4"""
	FSK4 = 0


# noinspection SpellCheckingInspection
class Detector(Enum):
	"""6 Members, AUTopeak ... SAMPle"""
	AUTopeak = 0
	AVERage = 1
	MAXPeak = 2
	MINPeak = 3
	RMS = 4
	SAMPle = 5


# noinspection SpellCheckingInspection
class DetectorSimple(Enum):
	"""2 Members, PEAK ... RMS"""
	PEAK = 0
	RMS = 1


# noinspection SpellCheckingInspection
class DialingMode(Enum):
	"""4 Members, DTMF ... SELCall"""
	DTMF = 0
	FDIaling = 1
	SCAL = 2
	SELCall = 3


# noinspection SpellCheckingInspection
class DigitalSource(Enum):
	"""8 Members, ARB ... ZIGBee"""
	ARB = 0
	DMR = 1
	DPMR = 2
	NXDN = 3
	P25 = 4
	POCSag = 5
	UDEFined = 6
	ZIGBee = 7


# noinspection SpellCheckingInspection
class DigitalToneMode(Enum):
	"""6 Members, DCS ... SELCall"""
	DCS = 0
	DTMF = 1
	FDIA = 2
	NONE = 3
	SCAL = 4
	SELCall = 5


# noinspection SpellCheckingInspection
class DirectionIo(Enum):
	"""2 Members, IN ... OUT"""
	IN = 0
	OUT = 1


# noinspection SpellCheckingInspection
class DirPwrSensorFwdValue(Enum):
	"""4 Members, CCDF ... PEP"""
	CCDF = 0
	CFAC = 1
	FPWR = 2
	PEP = 3


# noinspection SpellCheckingInspection
class DirPwrSensorRevValue(Enum):
	"""4 Members, REFL ... SWR"""
	REFL = 0
	RLOS = 1
	RPWR = 2
	SWR = 3


# noinspection SpellCheckingInspection
class DisplayLanguage(Enum):
	"""14 Members, AR ... ZH"""
	AR = 0
	CS = 1
	DA = 2
	DE = 3
	EN = 4
	ES = 5
	FR = 6
	IT = 7
	JA = 8
	KO = 9
	RU = 10
	SV = 11
	TR = 12
	ZH = 13


# noinspection SpellCheckingInspection
class DmrPattern(Enum):
	"""16 Members, BPRB15 ... SILence"""
	BPRB15 = 0
	BPRB9 = 1
	C153 = 2
	O153 = 3
	P1031 = 4
	PRBS9 = 5
	R10A = 6
	RA0 = 7
	RA1 = 8
	RFBS = 9
	RFMS = 10
	RLD = 11
	RPRB15 = 12
	RPRB9 = 13
	RSYR = 14
	SILence = 15


# noinspection SpellCheckingInspection
class DmrPatternB(Enum):
	"""3 Members, P1031 ... SYNC"""
	P1031 = 0
	SILence = 1
	SYNC = 2


# noinspection SpellCheckingInspection
class Dstrategy(Enum):
	"""2 Members, BYLayout ... OFF"""
	BYLayout = 0
	OFF = 1


# noinspection SpellCheckingInspection
class Eformat(Enum):
	"""2 Members, ASCii ... XML"""
	ASCii = 0
	XML = 1


# noinspection SpellCheckingInspection
class EstartMode(Enum):
	"""2 Members, AUTO ... EXPLicit"""
	AUTO = 0
	EXPLicit = 1


# noinspection SpellCheckingInspection
class EstopMode(Enum):
	"""4 Members, AUTO ... EXPLicit"""
	AUTO = 0
	BUFFerfull = 1
	ERRor = 2
	EXPLicit = 3


# noinspection SpellCheckingInspection
class ExpFrequency(Enum):
	"""2 Members, CONF ... FGEN"""
	CONF = 0
	FGEN = 1


# noinspection SpellCheckingInspection
class ExpressionMode(Enum):
	"""2 Members, REGex ... STRing"""
	REGex = 0
	STRing = 1


# noinspection SpellCheckingInspection
class ExtPwrSensorApp(Enum):
	"""2 Members, EPS ... NRTZ"""
	EPS = 0
	NRTZ = 1


# noinspection SpellCheckingInspection
class ExtSensorResolution(Enum):
	"""4 Members, PD0 ... PD3"""
	PD0 = 0
	PD1 = 1
	PD2 = 2
	PD3 = 3


# noinspection SpellCheckingInspection
class FftLength(Enum):
	"""3 Members, F16K ... F8K"""
	F16K = 0
	F4K = 1
	F8K = 2


# noinspection SpellCheckingInspection
class FftOffsetMode(Enum):
	"""2 Members, FIXed ... VARiable"""
	FIXed = 0
	VARiable = 1


# noinspection SpellCheckingInspection
class FftSpan(Enum):
	"""4 Members, SP1 ... SP5"""
	SP1 = 0
	SP10 = 1
	SP21 = 2
	SP5 = 3


# noinspection SpellCheckingInspection
class FftWindowType(Enum):
	"""5 Members, BLHA ... RECTangle"""
	BLHA = 0
	FLTP = 1
	HAMMing = 2
	HANN = 3
	RECTangle = 4


# noinspection SpellCheckingInspection
class FileSave(Enum):
	"""3 Members, OFF ... ONLY"""
	OFF = 0
	ON = 1
	ONLY = 2


# noinspection SpellCheckingInspection
class FilterDigital(Enum):
	"""4 Members, COSine ... SINC"""
	COSine = 0
	GAUSs = 1
	RRC = 2
	SINC = 3


# noinspection SpellCheckingInspection
class FilterNxDn(Enum):
	"""1 Members, NXTX ... NXTX"""
	NXTX = 0


# noinspection SpellCheckingInspection
class FilterType(Enum):
	"""5 Members, BANDpass ... WCDMa"""
	BANDpass = 0
	CDMA = 1
	GAUSs = 2
	TDSCdma = 3
	WCDMa = 4


# noinspection SpellCheckingInspection
class FreqCounterMode(Enum):
	"""2 Members, HW ... SW"""
	HW = 0
	SW = 1


# noinspection SpellCheckingInspection
class FskMode(Enum):
	"""2 Members, FSK2 ... FSK4"""
	FSK2 = 0
	FSK4 = 1


# noinspection SpellCheckingInspection
class GeneratorCoupling(Enum):
	"""5 Members, GEN1 ... OFF"""
	GEN1 = 0
	GEN2 = 1
	GEN3 = 2
	GEN4 = 3
	OFF = 4


# noinspection SpellCheckingInspection
class GeneratorCouplingVoIp(Enum):
	"""3 Members, GEN3 ... OFF"""
	GEN3 = 0
	GEN4 = 1
	OFF = 2


# noinspection SpellCheckingInspection
class GeneratorFilter(Enum):
	"""5 Members, COS ... SINC"""
	COS = 0
	GAUSs = 1
	RC = 2
	RRC = 3
	SINC = 4


# noinspection SpellCheckingInspection
class GeneratorState(Enum):
	"""7 Members, ADJusted ... PENDing"""
	ADJusted = 0
	AUTonomous = 1
	COUPled = 2
	INValid = 3
	OFF = 4
	ON = 5
	PENDing = 6


# noinspection SpellCheckingInspection
class HighpassFilter(Enum):
	"""2 Members, F300 ... OFF"""
	F300 = 0
	OFF = 1


# noinspection SpellCheckingInspection
class HighpassFilterExtended(Enum):
	"""4 Members, F300 ... OFF"""
	F300 = 0
	F50 = 1
	F6 = 2
	OFF = 3


# noinspection SpellCheckingInspection
class IlsLetter(Enum):
	"""2 Members, X ... Y"""
	X = 0
	Y = 1


# noinspection SpellCheckingInspection
class IlsTab(Enum):
	"""2 Members, GSLope ... LOCalizer"""
	GSLope = 0
	LOCalizer = 1


# noinspection SpellCheckingInspection
class Impedance(Enum):
	"""5 Members, IHOL ... R600"""
	IHOL = 0
	R150 = 1
	R300 = 2
	R50 = 3
	R600 = 4


# noinspection SpellCheckingInspection
class ImpulseLength(Enum):
	"""5 Members, T ... T8"""
	T = 0
	T2 = 1
	T4 = 2
	T6 = 3
	T8 = 4


# noinspection SpellCheckingInspection
class InputConnector(Enum):
	"""2 Members, RFCom ... RFIN"""
	RFCom = 0
	RFIN = 1


# noinspection SpellCheckingInspection
class InterfererMode(Enum):
	"""5 Members, AM ... PM"""
	AM = 0
	CW = 1
	FM = 2
	NONE = 3
	PM = 4


# noinspection SpellCheckingInspection
class IqFormat(Enum):
	"""2 Members, IQ ... RPHI"""
	IQ = 0
	RPHI = 1


# noinspection SpellCheckingInspection
class LeftRightDirection(Enum):
	"""2 Members, LEFT ... RIGHt"""
	LEFT = 0
	RIGHt = 1


# noinspection SpellCheckingInspection
class LevelEditMode(Enum):
	"""2 Members, INDividual ... TOTal"""
	INDividual = 0
	TOTal = 1


# noinspection SpellCheckingInspection
class LinkDirectionDmr(Enum):
	"""1 Members, MSSourced ... MSSourced"""
	MSSourced = 0


# noinspection SpellCheckingInspection
class LinkDirectionTetra(Enum):
	"""2 Members, DLNK ... ULNK"""
	DLNK = 0
	ULNK = 1


# noinspection SpellCheckingInspection
class LockRangeExternal(Enum):
	"""4 Members, INV ... WIDE"""
	INV = 0
	MEDium = 1
	NARRow = 2
	WIDE = 3


# noinspection SpellCheckingInspection
class LockRangeInternal(Enum):
	"""3 Members, INV ... NARRow"""
	INV = 0
	MEDium = 1
	NARRow = 2


# noinspection SpellCheckingInspection
class LowHigh(Enum):
	"""2 Members, HIGH ... LOW"""
	HIGH = 0
	LOW = 1


# noinspection SpellCheckingInspection
class LowpassFilter(Enum):
	"""4 Members, F15K ... OFF"""
	F15K = 0
	F3K = 1
	F4K = 2
	OFF = 3


# noinspection SpellCheckingInspection
class LowpassFilterExtended(Enum):
	"""6 Members, F15K ... OFF"""
	F15K = 0
	F255 = 1
	F3K = 2
	F3K4 = 3
	F4K = 4
	OFF = 5


# noinspection SpellCheckingInspection
class LteChannelBandwidth(Enum):
	"""4 Members, F10M ... F5M"""
	F10M = 0
	F20M = 1
	F3M = 2
	F5M = 3


# noinspection SpellCheckingInspection
class MagnitudeUnit(Enum):
	"""2 Members, RAW ... VOLT"""
	RAW = 0
	VOLT = 1


# noinspection SpellCheckingInspection
class MarkerFunction(Enum):
	"""6 Members, MAX ... MIN"""
	MAX = 0
	MAXL = 1
	MAXN = 2
	MAXR = 3
	MAXV = 4
	MIN = 5


# noinspection SpellCheckingInspection
class MarkerPlacement(Enum):
	"""2 Members, ABSolute ... RELative"""
	ABSolute = 0
	RELative = 1


# noinspection SpellCheckingInspection
class MeasAccuracy(Enum):
	"""2 Members, HIGH ... NORMal"""
	HIGH = 0
	NORMal = 1


# noinspection SpellCheckingInspection
class MeasState(Enum):
	"""10 Members, ACTive ... RUN"""
	ACTive = 0
	ADJusted = 1
	ALIVe = 2
	FROZen = 3
	INValid = 4
	OFF = 5
	PENDing = 6
	QUEued = 7
	RDY = 8
	RUN = 9


# noinspection SpellCheckingInspection
class ModeTetra(Enum):
	"""1 Members, DQPS45 ... DQPS45"""
	DQPS45 = 0


# noinspection SpellCheckingInspection
class ModulationScheme(Enum):
	"""8 Members, AM ... USB"""
	AM = 0
	ARB = 1
	CW = 2
	FM = 3
	FMSTereo = 4
	LSB = 5
	PM = 6
	USB = 7


# noinspection SpellCheckingInspection
class NotchPath(Enum):
	"""3 Members, AF ... VOIP"""
	AF = 0
	SPDif = 1
	VOIP = 2


# noinspection SpellCheckingInspection
class NrtDevice(Enum):
	"""3 Members, N14 ... N44"""
	N14 = 0
	N43 = 1
	N44 = 2


# noinspection SpellCheckingInspection
class NxdnPattern(Enum):
	"""14 Members, P1011 ... SILence"""
	P1011 = 0
	P1031 = 1
	PRBS15 = 2
	PRBS9 = 3
	R10A = 4
	RA0 = 5
	RA1 = 6
	RAW1 = 7
	RAW2 = 8
	RLD = 9
	RPRB15 = 10
	RPRB9 = 11
	RSYR = 12
	SILence = 13


# noinspection SpellCheckingInspection
class NxdnPatternB(Enum):
	"""13 Members, CUST ... STD1"""
	CUST = 0
	P1031 = 1
	PRBS9 = 2
	R1031 = 3
	R10A = 4
	RA0 = 5
	RA1 = 6
	RLD = 7
	RPRB15 = 8
	RPRB9 = 9
	RSYR = 10
	SILence = 11
	STD1 = 12


# noinspection SpellCheckingInspection
class OperationMode(Enum):
	"""2 Members, LOCal ... REMote"""
	LOCal = 0
	REMote = 1


# noinspection SpellCheckingInspection
class OptionsProductType(Enum):
	"""5 Members, ALL ... SWPackage"""
	ALL = 0
	FWA = 1
	HWOPtion = 2
	SWOPtion = 3
	SWPackage = 4


# noinspection SpellCheckingInspection
class OptionsScope(Enum):
	"""2 Members, INSTrument ... SYSTem"""
	INSTrument = 0
	SYSTem = 1


# noinspection SpellCheckingInspection
class OptionValidity(Enum):
	"""4 Members, ALL ... VALid"""
	ALL = 0
	CLICense = 1
	FUNCtional = 2
	VALid = 3


# noinspection SpellCheckingInspection
class OscillatorType(Enum):
	"""2 Members, OCXO ... TCXO"""
	OCXO = 0
	TCXO = 1


# noinspection SpellCheckingInspection
class OutputConnector(Enum):
	"""2 Members, RFCom ... RFOut"""
	RFCom = 0
	RFOut = 1


# noinspection SpellCheckingInspection
class OverviewType(Enum):
	"""3 Members, FFT ... OSCilloscope"""
	FFT = 0
	NONE = 1
	OSCilloscope = 2


# noinspection SpellCheckingInspection
class P25Mode(Enum):
	"""2 Members, C4FM ... CQPSk"""
	C4FM = 0
	CQPSk = 1


# noinspection SpellCheckingInspection
class P25Pattern(Enum):
	"""15 Members, BUSY ... SILence"""
	BUSY = 0
	C4FM = 1
	CALibration = 2
	IDLE = 3
	INTerference = 4
	P1011 = 5
	R10A = 6
	RA0 = 7
	RA1 = 8
	RAW1 = 9
	RLD = 10
	RPRB15 = 11
	RPRB9 = 12
	RSYR = 13
	SILence = 14


# noinspection SpellCheckingInspection
class PagerType(Enum):
	"""3 Members, ALPHanumeric ... TONLy"""
	ALPHanumeric = 0
	NUMeric = 1
	TONLy = 2


# noinspection SpellCheckingInspection
class PathCoupling(Enum):
	"""2 Members, AC ... DC"""
	AC = 0
	DC = 1


# noinspection SpellCheckingInspection
class PatternTetra(Enum):
	"""3 Members, S1 ... S3"""
	S1 = 0
	S2 = 1
	S3 = 2


# noinspection SpellCheckingInspection
class PayloadTypeTetra(Enum):
	"""5 Members, ALLO ... USER"""
	ALLO = 0
	ALLZero = 1
	ALTE = 2
	PRBS9 = 3
	USER = 4


# noinspection SpellCheckingInspection
class PowerMode(Enum):
	"""4 Members, ALL ... SWEep"""
	ALL = 0
	ONCE = 1
	PRESelect = 2
	SWEep = 3


# noinspection SpellCheckingInspection
class PowerSignalDirection(Enum):
	"""3 Members, AUTO ... REV"""
	AUTO = 0
	FWD = 1
	REV = 2


# noinspection SpellCheckingInspection
class PreDeEmphasis(Enum):
	"""4 Members, OFF ... T750"""
	OFF = 0
	T50 = 1
	T75 = 2
	T750 = 3


# noinspection SpellCheckingInspection
class ProtocolMode(Enum):
	"""3 Members, AGILent ... RAW"""
	AGILent = 0
	IEEE1174 = 1
	RAW = 2


# noinspection SpellCheckingInspection
class PtFiveFilter(Enum):
	"""2 Members, C4FM ... RC"""
	C4FM = 0
	RC = 1


# noinspection SpellCheckingInspection
class PulseShapingFilter(Enum):
	"""1 Members, RRC ... RRC"""
	RRC = 0


# noinspection SpellCheckingInspection
class PulseShapingUserFilter(Enum):
	"""5 Members, COS ... SINC"""
	COS = 0
	GAUSs = 1
	NXRX = 2
	RRC = 3
	SINC = 4


# noinspection SpellCheckingInspection
class PwrFilterType(Enum):
	"""2 Members, NARRow ... WIDE"""
	NARRow = 0
	WIDE = 1


# noinspection SpellCheckingInspection
class RbwFilterType(Enum):
	"""2 Members, BANDpass ... GAUSs"""
	BANDpass = 0
	GAUSs = 1


# noinspection SpellCheckingInspection
class RefFreqSource(Enum):
	"""3 Members, EXTernal ... INV"""
	EXTernal = 0
	INTernal = 1
	INV = 2


# noinspection SpellCheckingInspection
class Relative(Enum):
	"""2 Members, CONStant ... RELative"""
	CONStant = 0
	RELative = 1


# noinspection SpellCheckingInspection
class Repeat(Enum):
	"""2 Members, CONTinuous ... SINGleshot"""
	CONTinuous = 0
	SINGleshot = 1


# noinspection SpellCheckingInspection
class RepeatMode(Enum):
	"""2 Members, CONTinuous ... SINGle"""
	CONTinuous = 0
	SINGle = 1


# noinspection SpellCheckingInspection
class ResourceState(Enum):
	"""8 Members, ACTive ... RUN"""
	ACTive = 0
	ADJusted = 1
	INValid = 2
	OFF = 3
	PENDing = 4
	QUEued = 5
	RDY = 6
	RUN = 7


# noinspection SpellCheckingInspection
class ResultStatus(Enum):
	"""11 Members, DC ... ULEU"""
	DC = 0
	INV = 1
	NAV = 2
	NCAP = 3
	OFF = 4
	OFL = 5
	OK = 6
	ON = 7
	UFL = 8
	ULEL = 9
	ULEU = 10


# noinspection SpellCheckingInspection
class ScreenshotFormat(Enum):
	"""3 Members, BMP ... PNG"""
	BMP = 0
	JPG = 1
	PNG = 2


# noinspection SpellCheckingInspection
class SearchExtent(Enum):
	"""3 Members, FULL ... ONLevel"""
	FULL = 0
	OFFLevel = 1
	ONLevel = 2


# noinspection SpellCheckingInspection
class SearchRoutine(Enum):
	"""6 Members, ADELay ... TSENsitivity"""
	ADELay = 0
	RIFBandwidth = 1
	RSENsitivity = 2
	RSQuelch = 3
	SSNR = 4
	TSENsitivity = 5


# noinspection SpellCheckingInspection
class SearchRoutinePath(Enum):
	"""3 Members, AFI1 ... VOIP"""
	AFI1 = 0
	AFI2 = 1
	VOIP = 2


# noinspection SpellCheckingInspection
class SelCallStandard(Enum):
	"""8 Members, CCIR ... ZVEI3"""
	CCIR = 0
	DZVei = 1
	EEA = 2
	EIA = 3
	PZVei = 4
	ZVEI1 = 5
	ZVEI2 = 6
	ZVEI3 = 7


# noinspection SpellCheckingInspection
class SharingModeTetra(Enum):
	"""4 Members, CARRier ... TRAFfic"""
	CARRier = 0
	CONTinuous = 1
	MMCH = 2
	TRAFfic = 3


# noinspection SpellCheckingInspection
class SignalSlope(Enum):
	"""2 Members, FEDGe ... REDGe"""
	FEDGe = 0
	REDGe = 1


# noinspection SpellCheckingInspection
class SignalSlopeExt(Enum):
	"""4 Members, FALLing ... RISing"""
	FALLing = 0
	FEDGe = 1
	REDGe = 2
	RISing = 3


# noinspection SpellCheckingInspection
class SignalSource(Enum):
	"""14 Members, AFI1 ... SPIR"""
	AFI1 = 0
	AFI2 = 1
	AFIB = 2
	FCHL = 3
	FCHR = 4
	FILE = 5
	GEN1 = 6
	GEN2 = 7
	GEN3 = 8
	GEN4 = 9
	GENB = 10
	SPIL = 11
	SPIN = 12
	SPIR = 13


# noinspection SpellCheckingInspection
class SingDualTonesType(Enum):
	"""2 Members, DTONes ... STONes"""
	DTONes = 0
	STONes = 1


# noinspection SpellCheckingInspection
class SingDualToneType(Enum):
	"""2 Members, DTONe ... STONe"""
	DTONe = 0
	STONe = 1


# noinspection SpellCheckingInspection
class SipState(Enum):
	"""3 Members, ERRor ... TERMinated"""
	ERRor = 0
	ESTablished = 1
	TERMinated = 2


# noinspection SpellCheckingInspection
class SoundSource(Enum):
	"""6 Members, AFONe ... SPDif"""
	AFONe = 0
	DEModulator = 1
	GENone = 2
	GENThree = 3
	LAN = 4
	SPDif = 5


# noinspection SpellCheckingInspection
class SpanMode(Enum):
	"""2 Members, FSWeep ... ZSPan"""
	FSWeep = 0
	ZSPan = 1


# noinspection SpellCheckingInspection
class SpecAnApp(Enum):
	"""2 Members, FREQ ... ZERO"""
	FREQ = 0
	ZERO = 1


# noinspection SpellCheckingInspection
class Standard(Enum):
	"""8 Members, CUSTom ... TETRa"""
	CUSTom = 0
	DMR = 1
	DPMR = 2
	LTE = 3
	NXDN = 4
	P25 = 5
	SPECtrum = 6
	TETRa = 7


# noinspection SpellCheckingInspection
class StandardDigital(Enum):
	"""2 Members, DMR ... TETRa"""
	DMR = 0
	TETRa = 1


# noinspection SpellCheckingInspection
class Statistic(Enum):
	"""4 Members, AVERage ... MINimum"""
	AVERage = 0
	CURRent = 1
	MAXimum = 2
	MINimum = 3


# noinspection SpellCheckingInspection
class StatRegFormat(Enum):
	"""4 Members, ASCii ... OCTal"""
	ASCii = 0
	BINary = 1
	HEXadecimal = 2
	OCTal = 3


# noinspection SpellCheckingInspection
class Status(Enum):
	"""2 Members, FAILed ... PASSed"""
	FAILed = 0
	PASSed = 1


# noinspection SpellCheckingInspection
class StopCondition(Enum):
	"""2 Members, NONE ... SLFail"""
	NONE = 0
	SLFail = 1


# noinspection SpellCheckingInspection
class SubTab(Enum):
	"""9 Members, AFResults ... TRIM"""
	AFResults = 0
	FFT = 1
	FMSTereo = 2
	MULTitone = 3
	OSC = 4
	OVERview = 5
	RFResults = 6
	TONes = 7
	TRIM = 8


# noinspection SpellCheckingInspection
class SubTabAudioMeas(Enum):
	"""5 Members, AFResults ... TRIM"""
	AFResults = 0
	FFT = 1
	OSC = 2
	OVERview = 3
	TRIM = 4


# noinspection SpellCheckingInspection
class SubTabDigitalMeas(Enum):
	"""3 Members, BER ... SINFo"""
	BER = 0
	OVERview = 1
	SINFo = 2


# noinspection SpellCheckingInspection
class SubTabRoutines(Enum):
	"""2 Members, CHARt ... TABLe"""
	CHARt = 0
	TABLe = 1


# noinspection SpellCheckingInspection
class SubTabVseMeas(Enum):
	"""11 Members, CONStellation ... SYMResults"""
	CONStellation = 0
	DEMod = 1
	EYEDiagram = 2
	LTE = 3
	NXDNresults = 4
	OVERview = 5
	PVTResults = 6
	RFResults = 7
	SPECtrum = 8
	SYMDistr = 9
	SYMResults = 10


# noinspection SpellCheckingInspection
class SupplyMode(Enum):
	"""2 Members, BATTery ... MAINs"""
	BATTery = 0
	MAINs = 1


# noinspection SpellCheckingInspection
class TabSplit(Enum):
	"""2 Members, SPLit ... TAB"""
	SPLit = 0
	TAB = 1


# noinspection SpellCheckingInspection
class TargetParameter(Enum):
	"""5 Members, NPEK ... RMSQ"""
	NPEK = 0
	PNPA = 1
	PPEK = 2
	RMS = 3
	RMSQ = 4


# noinspection SpellCheckingInspection
class TargetParType(Enum):
	"""4 Members, SINad ... SNRatio"""
	SINad = 0
	SNDNratio = 1
	SNNRatio = 2
	SNRatio = 3


# noinspection SpellCheckingInspection
class TestModeTetra(Enum):
	"""3 Members, SIDecoding ... VSE"""
	SIDecoding = 0
	T1 = 1
	VSE = 2


# noinspection SpellCheckingInspection
class TestPlanState(Enum):
	"""10 Members, EDITmode ... SERRor"""
	EDITmode = 0
	FINished = 1
	IDLE = 2
	LOADing = 3
	NOAVailable = 4
	NOLoaded = 5
	OPTMissing = 6
	PAUSed = 7
	RUNNing = 8
	SERRor = 9


# noinspection SpellCheckingInspection
class TimeoutMode(Enum):
	"""2 Members, AUTO ... MANU"""
	AUTO = 0
	MANU = 1


# noinspection SpellCheckingInspection
class ToneMode(Enum):
	"""4 Members, NOISe ... STONe"""
	NOISe = 0
	NONE = 1
	SQUare = 2
	STONe = 3


# noinspection SpellCheckingInspection
class ToneTypeA(Enum):
	"""9 Members, DTMF ... STONe"""
	DTMF = 0
	DTONe = 1
	FDIaling = 2
	MTONe = 3
	NOISe = 4
	SCAL = 5
	SELCall = 6
	SQUare = 7
	STONe = 8


# noinspection SpellCheckingInspection
class ToneTypeB(Enum):
	"""4 Members, CTCSs ... SUBTone"""
	CTCSs = 0
	DCS = 1
	NONE = 2
	SUBTone = 3


# noinspection SpellCheckingInspection
class TraceB(Enum):
	"""5 Members, AVERage ... TDOMmain"""
	AVERage = 0
	CURRent = 1
	MAXimum = 2
	MINimum = 3
	TDOMmain = 4


# noinspection SpellCheckingInspection
class TraceC(Enum):
	"""3 Members, AVERage ... MAXimum"""
	AVERage = 0
	CURRent = 1
	MAXimum = 2


# noinspection SpellCheckingInspection
class Transmission(Enum):
	"""3 Members, EFR9600 ... EHR9600"""
	EFR9600 = 0
	EHR4800 = 1
	EHR9600 = 2


# noinspection SpellCheckingInspection
class TriggerCouplingAin(Enum):
	"""4 Members, DEMod ... VOIP"""
	DEMod = 0
	NONE = 1
	SIN = 2
	VOIP = 3


# noinspection SpellCheckingInspection
class TriggerCouplingDemod(Enum):
	"""4 Members, AIN ... VOIP"""
	AIN = 0
	NONE = 1
	SIN = 2
	VOIP = 3


# noinspection SpellCheckingInspection
class TriggerCouplingDigital(Enum):
	"""3 Members, AIN ... NONE"""
	AIN = 0
	DEMod = 1
	NONE = 2


# noinspection SpellCheckingInspection
class TriggerMode(Enum):
	"""4 Members, AUTO ... SINGle"""
	AUTO = 0
	FRUN = 1
	NORMal = 2
	SINGle = 3


# noinspection SpellCheckingInspection
class TriggerSourceAf(Enum):
	"""2 Members, AF1 ... AF2"""
	AF1 = 0
	AF2 = 1


# noinspection SpellCheckingInspection
class TriggerSourceDemod(Enum):
	"""3 Members, DEMod ... RIGHt"""
	DEMod = 0
	LEFT = 1
	RIGHt = 2


# noinspection SpellCheckingInspection
class TtlInterface(Enum):
	"""2 Members, WIRE1 ... WIRE2"""
	WIRE1 = 0
	WIRE2 = 1


# noinspection SpellCheckingInspection
class TxAfSource(Enum):
	"""3 Members, AF1O ... VOIP"""
	AF1O = 0
	AF2O = 1
	VOIP = 2


# noinspection SpellCheckingInspection
class UpDownDirection(Enum):
	"""2 Members, DOWN ... UP"""
	DOWN = 0
	UP = 1


# noinspection SpellCheckingInspection
class UserDefPattern(Enum):
	"""2 Members, PRBS6 ... PRBS9"""
	PRBS6 = 0
	PRBS9 = 1


# noinspection SpellCheckingInspection
class UserRole(Enum):
	"""5 Members, ADMin ... USER"""
	ADMin = 0
	DEVeloper = 1
	SERVice = 2
	UEXTended = 3
	USER = 4


# noinspection SpellCheckingInspection
class VoIpCodec(Enum):
	"""2 Members, ALAW ... ULAW"""
	ALAW = 0
	ULAW = 1


# noinspection SpellCheckingInspection
class VoIpSource(Enum):
	"""4 Members, AFI1 ... GEN4"""
	AFI1 = 0
	AFI2 = 1
	GEN3 = 2
	GEN4 = 3


# noinspection SpellCheckingInspection
class VphaseDirection(Enum):
	"""2 Members, FROM ... TO"""
	FROM = 0
	TO = 1


# noinspection SpellCheckingInspection
class WeightingFilter(Enum):
	"""4 Members, AWEighting ... OFF"""
	AWEighting = 0
	CCITt = 1
	CMESsage = 2
	OFF = 3


# noinspection SpellCheckingInspection
class Xdivision(Enum):
	"""19 Members, M1 ... U500"""
	M1 = 0
	M10 = 1
	M100 = 2
	M2 = 3
	M20 = 4
	M200 = 5
	M5 = 6
	M50 = 7
	M500 = 8
	S1 = 9
	U1 = 10
	U10 = 11
	U100 = 12
	U2 = 13
	U20 = 14
	U200 = 15
	U5 = 16
	U50 = 17
	U500 = 18


# noinspection SpellCheckingInspection
class XrtInputConnector(Enum):
	"""8 Members, RF1 ... RF8"""
	RF1 = 0
	RF2 = 1
	RF3 = 2
	RF4 = 3
	RF5 = 4
	RF6 = 5
	RF7 = 6
	RF8 = 7


# noinspection SpellCheckingInspection
class YesNoStatus(Enum):
	"""2 Members, NO ... YES"""
	NO = 0
	YES = 1


# noinspection SpellCheckingInspection
class ZigBeeMode(Enum):
	"""1 Members, OQPSk ... OQPSk"""
	OQPSk = 0
