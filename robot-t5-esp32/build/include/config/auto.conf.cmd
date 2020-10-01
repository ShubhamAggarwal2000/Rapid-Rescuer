deps_config := \
	/home/gaurav4857/esp/esp-idf/components/app_trace/Kconfig \
	/home/gaurav4857/esp/esp-idf/components/aws_iot/Kconfig \
	/home/gaurav4857/esp/esp-idf/components/bt/Kconfig \
	/home/gaurav4857/esp/esp-idf/components/driver/Kconfig \
	/home/gaurav4857/esp/esp-idf/components/efuse/Kconfig \
	/home/gaurav4857/esp/esp-idf/components/esp32/Kconfig \
	/home/gaurav4857/esp/esp-idf/components/esp_adc_cal/Kconfig \
	/home/gaurav4857/esp/esp-idf/components/esp_event/Kconfig \
	/home/gaurav4857/esp/esp-idf/components/esp_http_client/Kconfig \
	/home/gaurav4857/esp/esp-idf/components/esp_http_server/Kconfig \
	/home/gaurav4857/esp/esp-idf/components/esp_https_ota/Kconfig \
	/home/gaurav4857/esp/esp-idf/components/espcoredump/Kconfig \
	/home/gaurav4857/esp/esp-idf/components/ethernet/Kconfig \
	/home/gaurav4857/esp/esp-idf/components/fatfs/Kconfig \
	/home/gaurav4857/esp/esp-idf/components/freemodbus/Kconfig \
	/home/gaurav4857/esp/esp-idf/components/freertos/Kconfig \
	/home/gaurav4857/esp/esp-idf/components/heap/Kconfig \
	/home/gaurav4857/esp/esp-idf/components/libsodium/Kconfig \
	/home/gaurav4857/esp/esp-idf/components/log/Kconfig \
	/home/gaurav4857/esp/esp-idf/components/lwip/Kconfig \
	/home/gaurav4857/esp/esp-idf/components/mbedtls/Kconfig \
	/home/gaurav4857/esp/esp-idf/components/mdns/Kconfig \
	/home/gaurav4857/esp/esp-idf/components/mqtt/Kconfig \
	/home/gaurav4857/esp/esp-idf/components/nvs_flash/Kconfig \
	/home/gaurav4857/esp/esp-idf/components/openssl/Kconfig \
	/home/gaurav4857/esp/esp-idf/components/pthread/Kconfig \
	/home/gaurav4857/esp/esp-idf/components/spi_flash/Kconfig \
	/home/gaurav4857/esp/esp-idf/components/spiffs/Kconfig \
	/home/gaurav4857/esp/esp-idf/components/tcpip_adapter/Kconfig \
	/home/gaurav4857/esp/esp-idf/components/unity/Kconfig \
	/home/gaurav4857/esp/esp-idf/components/vfs/Kconfig \
	/home/gaurav4857/esp/esp-idf/components/wear_levelling/Kconfig \
	/home/gaurav4857/esp/esp-idf/components/wifi_provisioning/Kconfig \
	/home/gaurav4857/esp/esp-idf/components/app_update/Kconfig.projbuild \
	/home/gaurav4857/esp/esp-idf/components/bootloader/Kconfig.projbuild \
	/home/gaurav4857/esp/esp-idf/components/esptool_py/Kconfig.projbuild \
	/home/gaurav4857/Documents/robot-t4-esp32/main/Kconfig.projbuild \
	/home/gaurav4857/esp/esp-idf/components/partition_table/Kconfig.projbuild \
	/home/gaurav4857/esp/esp-idf/Kconfig

include/config/auto.conf: \
	$(deps_config)

ifneq "$(IDF_TARGET)" "esp32"
include/config/auto.conf: FORCE
endif
ifneq "$(IDF_CMAKE)" "n"
include/config/auto.conf: FORCE
endif

$(deps_config): ;
