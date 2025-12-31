# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [0.1.0] - 2025-12-31

### Added
- Initial release of Django Fake Filler
- Automatic fake data generation for Django models
- Support for all standard Django field types
- Smart field name mapping (email, username, phone, etc.)
- Foreign key relationship handling
- OneToOne relationship handling
- ManyToMany relationship handling
- Management command `fakes` for generating data
- Command options: `--all`, `--models`, `--num`, `--m2m`
- Progress bars with tqdm integration
- Safe unique field handling
- Configurable field mappings
- Model and app exclusion support
- Comprehensive documentation
- MIT License

### Features
- Intelligent field type detection
- Automatic related object creation
- Locale support via Faker
- Password hashing for user models
- Slug generation
- UUID generation
- JSON field support

## [Unreleased]

### Planned
- Custom faker provider support
- Configuration file support
- Django admin integration
- Bulk creation optimization
- Command to clear generated data
- More field mapping presets
- Documentation website

---

[0.1.0]: https://github.com/yourusername/django-fake-filler/releases/tag/v0.1.0
