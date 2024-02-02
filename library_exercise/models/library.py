from odoo import api, fields, models
import logging

_logger = logging.getLogger(__name__)

class LibraryGenre(models.Model):
    _name = "library.genre"
    _description = "Ganre for the book"

    name = fields.Char(String="Genre", required=True)

class LibraryBook(models.Model):
    _name = "library.book"
    _description = "Basic book"

    title = fields.Char(string='Title', required=True)
    description = fields.Char(string='Short description', required=True)
    pages = fields.Integer(string="Pages")
    genres = fields.Many2many('library.genre', string="Genres")

class LibraryLender(models.Model):
    _inherit = 'res.partner'
    _name = "library.lender"

    is_lender = fields.Boolean("Lender", default=True)
    lends = fields.One2many("library.lend", "user", string="Lends")
    channel_ids = fields.Many2many("mail.channel", "mail_channel_profile_partner", "partner_id", "channel_id", copy=False)
    #commercial_partner_id = fields.Char(string='fake', required=False)


class LibraryLend(models.Model):
    _name = "library.lend" 
    _description = "Basic library lending"

    user = fields.Many2one(comodel_name="library.lender")#, required=True, delegate=True)
    start = fields.Date(string='Start date')
    end = fields.Date(string='End date')
    books = fields.Many2many('library.book', string="Books")
    status = fields.Selection([
            ('reserved', 'Reserved'),
            ('lended', 'Lended'),
            ('returned', 'Returned'),
            ('cancelled', 'Cancelled')
            ], required=True)
    
    def check_expiry(self):
        _logger.info("OGHI: check expiry")
        today = fields.Date.today()
        all_lended = self.env["library.lend"].search([])
        _logger.info("OGHI: all_lended %s", all_lended)
        _logger.info("OGHI: mail mail  %s", self.env["mail.mail"])
        _logger.info("OGHI: env  %s", dict(self.env["library.email"]))
        
        for lend in all_lended:
            _logger.info("OGHI: %s not returned or cancelled, end=%s, user email=%s", lend.status, lend.end, lend.user.email)

            if lend.status!='returned' and lend.status!="cancelled" and lend.end < today and lend.user.email is not None:
                _logger.info("OGHI: INSIDE IF")    
                lend.write({"status": "cancelled"})

                
                mail_template = self.env['library.email'].browse("library_email")
                _logger.info("OGHI: %s ", mail_template)

                mail_template.write({'to': lend.user.email, "name": lend.user.name, "book": lend.books, "end": lend.end})

                if mail_template:
                    _logger.info("OGHI: sending an email")
                    mail_template.send_mail(self.id, force_send=True, raise_exception=True)
                else:
                    _logger.info("OGHI: NOT sending an email")

            else:
                _logger.info("OGHI: else")
        
class LibraryEmail(models.Model):
    _name = "library.email"

    to = fields.Char(String="To", required=True)
    name = fields.Char(String="Name")
    book = fields.Char(String="Book")
    end = fields.Date(string='End date')
