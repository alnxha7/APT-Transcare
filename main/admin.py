from django.contrib import admin
from .models import Brand, Vehicle, Vehicle_type, Vehicle_master, Employee_master, Trip_sheet, Table_Accountsmaster, \
    Table_Acntchild, VoucherConfiguration,Table_Companydetailsmaster,Table_companyDetailschild, Table_DrCrNote,Table_Acntchild,Table_Accountsmaster,Table_Voucher, Table_Contra_Entry, \
    Table_Journal_Entry, RateMaster, RateChild

# Register your models here.

admin.site.register(Brand)
admin.site.register(Vehicle)
admin.site.register(Vehicle_type)
# admin.site.register(Vehicle_master)
admin.site.register(Employee_master)
admin.site.register(Trip_sheet)

class RateChildInline(admin.TabularInline):
    model = RateChild
    extra = 1


@admin.register(RateMaster)
class RateMasterAdmin(admin.ModelAdmin):
    list_display = ("customer_name", "company", "branch")
    search_fields = ("customer_name", )
    list_filter = ("company", "branch")
    inlines = [RateChildInline]


@admin.register(RateChild)
class RateChildAdmin(admin.ModelAdmin):
    list_display = ("master", "district", "rate")
    search_fields = ("district", )
    list_filter = ("district", )


@admin.register(Vehicle_master)
class VehicleMasterAdmin(admin.ModelAdmin):
    list_display = ('registration_number', 'rc_owner_name')


admin.site.register(Table_Acntchild)
admin.site.register(Table_Accountsmaster)

@admin.register(VoucherConfiguration)
class VoucherConfigurationAdmin(admin.ModelAdmin):
    list_display = ('category', 'series', 'serial_no')
    search_fields = ('category', 'series')
    list_filter = ('category',)

class CompanydetailsmasterAdmin(admin.ModelAdmin):
    list_display = ('company_id', 'companyname', 'email', 'gst', 'pan')
    search_fields = ('company_id', 'companyname')

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if request.user.is_superuser:
            return qs
        return qs.filter(user=request.user)

class CompanyDetailschildAdmin(admin.ModelAdmin):
    list_display = ('company_id', 'fycode', 'finyearfrom', 'finyearto', 'databasename1')

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if request.user.is_superuser:
            return qs
        return qs.filter(company_id__user=request.user)

admin.site.register(Table_Companydetailsmaster, CompanydetailsmasterAdmin)
admin.site.register(Table_companyDetailschild, CompanyDetailschildAdmin)


from django.utils.html import format_html
from django.urls import reverse
from django.contrib import admin
from .models import Table_BillMaster, Table_BillItems

from django.contrib import admin
from .models import Table_BillMaster, Table_BillItems


# Inline: Show items inside Bill Master
class Table_BillItemsInline(admin.TabularInline):
    model = Table_BillItems
    extra = 1  # number of empty rows to display
    fields = (
        "vehicle_no", "vehicle_type", "total_km", "km_rate",
        "fixed_km", "additional_km", "total_charges",
        "additional_charge", "fixed_or_rental_charge",
        "toll_parking", "total"
    )
    readonly_fields = ("total",)  # total is usually calculated, not typed


# Bill Master Admin
@admin.register(Table_BillMaster)
class Table_BillMasterAdmin(admin.ModelAdmin):
    list_display = (
        "id", "bill_no", "bill_date", "customer", "bill_type",
        "rate_type", "grand_total", "total_gross", "amt_before_tax"
    )
    list_filter = (
        "bill_date", "rate_type", "bill_type", "gst_type", "branch"
    )
    search_fields = (
        "bill_no", "customer__account_name", "customer__account_code"
    )
    date_hierarchy = "bill_date"
    inlines = [Table_BillItemsInline]
    ordering = ("-bill_date", "-bill_no")

    fieldsets = (
        ("Bill Information", {
            "fields": (
                "user", "branch", "fy_code", "company", "series",
                "bill_no", "bill_date", "bill_type", "customer",
                "date_from", "date_to", "rate_type"
            )
        }),
        ("Discounts & Rounding", {
            "fields": (
                "sp_disc_perc", "sp_disc_amt", "round_off", "total_discounts"
            )
        }),
        ("Amounts", {
            "fields": (
                "total_gross", "amt_before_tax", "cgst", "sgst", "igst", "grand_total"
            )
        }),
        ("GST Details", {
            "fields": ("gst_type",),
        }),
    )


# Bill Items Admin (standalone view if needed)
@admin.register(Table_BillItems)
class Table_BillItemsAdmin(admin.ModelAdmin):
    list_display = (
        "id", "master", "vehicle_no", "vehicle_type",
        "total_km", "km_rate", "fixed_km", "additional_km",
        "total_charges", "additional_charge", "toll_parking", "total"
    )
    list_filter = ("vehicle_type",)
    search_fields = ("vehicle_no", "master__bill_no")
    ordering = ("master", "vehicle_no")




@admin.register(Table_DrCrNote)
class Table_DrCrNoteAdmin(admin.ModelAdmin):
    list_display = ("series", "noteno", "ndate", "accountcode", "narration", "dramount", "cramount", "ntype", "userid", "coid", "fycode", "brid")


class ContraEntryNoteAdmin(admin.ModelAdmin):
    list_display = ('series', 'voucher_no', 'vdate', 'accountcode', 'narration', 'dramount', 'cramount', 'user_id', 'coid', 'fycode', 'brid')

admin.site.register(Table_Contra_Entry, ContraEntryNoteAdmin)


class JournalEntryAdmin(admin.ModelAdmin):
    list_display = ('series', 'voucher_no', 'vdate', 'accountcode', 'narration', 'dramount', 'cramount', 'user_id', 'coid', 'fycode', 'brid')

admin.site.register(Table_Journal_Entry, JournalEntryAdmin)




class TableVoucherAdmin(admin.ModelAdmin):
    list_display = ('Series', 'VoucherNo', 'Vdate', 'Accountcode', 'Headcode', 'payment', 'VAmount', 'VType', 'Narration', 'CStatus', 'UserID', 'FYCode', 'Coid', 'Branch_ID')
    search_fields = ('Series', 'VoucherNo', 'Accountcode', 'Headcode', 'Narration')
    list_filter = ('Series', 'Vdate', 'VType', 'CStatus')

admin.site.register(Table_Voucher, TableVoucherAdmin)


from .models import LorryReceiptMaster, LorryReceiptItems


@admin.register(LorryReceiptMaster)
class LorryReceiptMasterAdmin(admin.ModelAdmin):
    list_display = (
        'id', 'lr_no', 'lr_date', 'company', 'branch', 'branch_to',
        'consigner_name', 'consignee_name', 'vehicle_no',
        'total_charges', 'grand_total'
    )
    list_filter = ('company', 'branch', 'lr_date')
    search_fields = ('lr_no', 'consigner_name', 'consignee_name', 'vehicle_no')
    date_hierarchy = 'lr_date'


@admin.register(LorryReceiptItems)
class LorryReceiptItemsAdmin(admin.ModelAdmin):
    list_display = (
        'id', 'master', 'checked', 'item_code', 'item', 'weight', 'rate', 'freight', 'pkg'
    )
    list_filter = ('master',)
    search_fields = ('item_code', 'item', 'pkg')

from .models import User
from django.contrib.auth.admin import UserAdmin

admin.site.register(User, UserAdmin)

from .models import CashReceipt, CashReceiptItems


@admin.register(CashReceipt)
class CashReceiptAdmin(admin.ModelAdmin):
    list_display = (
        'id', 'receipt_no', 'receipt_date', 'company', 'branch',
        'consigner_name', 'consignee_name', 'vehicle_no',
        'total_charges', 'grand_total'
    )
    list_filter = ('company', 'branch', 'receipt_date')
    search_fields = ('receipt_no', 'consigner_name', 'consignee_name', 'vehicle_no')
    date_hierarchy = 'receipt_date'


@admin.register(CashReceiptItems)
class CashReceiptItemsAdmin(admin.ModelAdmin):
    list_display = (
        'id', 'master', 'item_code', 'item', 'weight', 'rate', 'freight', 'pkg'
    )
    list_filter = ('master',)
    search_fields = ('item_code', 'item', 'pkg')