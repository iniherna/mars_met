import parser_report
import parser_magnitude
import xml.sax

parser_rep = xml.sax.make_parser()
handler_rep = parser_report.wr_handler()
parser_rep.setContentHandler(handler_rep)
parser_rep.parse("./example_data/rems_climate.xml")

parser_mag = xml.sax.make_parser()
handler_mag = parser_magnitude.wr_handler()
parser_mag.setContentHandler(handler_mag)
parser_mag.parse("./example_data/rems_climate.xml")