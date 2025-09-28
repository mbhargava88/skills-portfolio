package config

import "os"

// Config stores all configuration of the application.
// The values are read from environment variables.
type Config struct {
	DBDriver          string
	DBSource          string
	HTTPServerAddress string
	GRPCServerAddress string
	JWTSecret         string
}

// LoadConfig reads configuration from environment variables.
func LoadConfig(path string) (config Config, err error) {
	config.DBDriver = os.Getenv("DB_DRIVER")
	config.DBSource = os.Getenv("DB_SOURCE")
	config.HTTPServerAddress = os.Getenv("HTTP_SERVER_ADDRESS")
	config.GRPCServerAddress = os.Getenv("GRPC_SERVER_ADDRESS")
	config.JWTSecret = os.Getenv("JWT_SECRET")

	return
}
