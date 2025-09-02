package br.com.rotafood.api.infra.utils;

import java.time.Instant;
import java.time.LocalDate;
import java.time.LocalDateTime;
import java.time.ZoneId;
import java.time.format.DateTimeFormatter;
import java.time.format.DateTimeParseException;
import java.util.Date;

public class DateUtils {

    private static final ZoneId ZONE_BRAZIL = ZoneId.of("America/Sao_Paulo");
    private static final DateTimeFormatter BRAZILIAN_FORMATTER = DateTimeFormatter.ofPattern("dd/MM/yyyy HH:mm:ss").withZone(ZONE_BRAZIL);
    private static final DateTimeFormatter ISO_DATE_FORMATTER = DateTimeFormatter.ofPattern("yyyy-MM-dd");


    public static String formatToBrazilianTime(Instant instant) {
        return instant != null ? BRAZILIAN_FORMATTER.format(instant) : null;
    }


    public static Date convertInstantToDate(Instant instant) {
        return instant != null ? Date.from(instant.atZone(ZONE_BRAZIL).toInstant()) : null;
    }


    public static Instant convertDateToInstant(Date date) {
        return date != null ? date.toInstant() : null;
    }

    public static String formatDateToBrazilianTime(Date date) {
        return date != null ? formatToBrazilianTime(date.toInstant()) : null;
    }


    public static Instant parseDateStringToInstant(String dateStr, boolean endOfDay) {
        if (dateStr == null || dateStr.isBlank()) return null;
        try {
            LocalDate localDate = LocalDate.parse(dateStr, ISO_DATE_FORMATTER);
            LocalDateTime dateTime = endOfDay
                    ? localDate.atTime(23, 59, 59)
                    : localDate.atStartOfDay();
            return dateTime.atZone(ZONE_BRAZIL).toInstant();
        } catch (DateTimeParseException e) {
            throw new IllegalArgumentException("Invalid date format. Use 'yyyy-MM-dd'.", e);
        }
    }
}
