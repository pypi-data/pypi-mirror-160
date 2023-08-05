#pragma once

#include <mitsuba/mitsuba.h>
#include <mitsuba/core/logger.h>
#include <mitsuba/core/object.h>
#include <mitsuba/core/rfilter.h>
#include <mitsuba/core/vector.h>
#include <mitsuba/render/sampler.h>
#include <mitsuba/render/fwd.h>
#include <mitsuba/render/texture.h>

NAMESPACE_BEGIN(mitsuba)


/**
 * \brief This list of flags is used to classify the different types of films.
 */
enum class FilmFlags : uint32_t {
    // =============================================================
    //                      Emitter types
    // =============================================================

    /// No flags set (default value)
    Empty                = 0x0,

    /// The film stores an alpha channel
    Alpha                = 0x1,

    /// The film stores a spectral representation of the image
    Spectral             = 0x2,

    /**
     * The film provides a customized \ref prepare_sample() routine that implements
     * a special treatment of the samples before storing them in the Image Block.
     */
    Special              = 0x4,
};

MI_DECLARE_ENUM_OPERATORS(FilmFlags)


/** \brief Abstract film base class - used to store samples
 * generated by \ref Integrator implementations.
 *
 * To avoid lock-related bottlenecks when rendering with many cores,
 * rendering threads first store results in an "image block", which
 * is then committed to the film using the \ref put() method.
 */
template <typename Float, typename Spectrum>
class MI_EXPORT_LIB Film : public Object {
public:
    MI_IMPORT_TYPES(ImageBlock, ReconstructionFilter, Texture)

    /**
     * Configure the film for rendering a specified set of extra channels (AOVS).
     * Returns the total number of channels that the film will store
     */
    virtual size_t prepare(const std::vector<std::string> &aovs) = 0;

    /// Merge an image block into the film. This methods should be thread-safe.
    virtual void put_block(const ImageBlock *block) = 0;

    /// Return a image buffer object storing the developed image
    virtual TensorXf develop(bool raw = false) const = 0;

    /// Return a bitmap object storing the developed contents of the film
    virtual ref<Bitmap> bitmap(bool raw = false) const = 0;

    /// Write the developed contents of the film to a file on disk
    virtual void write(const fs::path &path) const = 0;

    /// dr::schedule() variables that represent the internal film storage
    virtual void schedule_storage() = 0;

    /**
      * \brief Prepare spectrum samples to be in the format expected by the film
      *
      * It will be used if the Film contains the ``Special`` flag enabled.
      *
      * This method should be applied with films that deviate from HDR film behavior.
      * Normally ``Films`` will store within the ``ImageBlock`` the samples following
      * an RGB shape. But ``Films`` may want to store the samples with other
      * structures (e.g. store several channels containing monochromatic information).
      * In that situation, this method allows transforming the sample format generated
      * by the integrators to the one that the Film will store inside the ImageBlock.
      *
      * \param spec
      *    Sample value associated with the specified wavelengths
      *
      * \param wavelengths
      *    Sample wavelengths in nanometers
      *
      * \param aovs
      *    Points to an array of length equal to the number of spectral sensitivities
      *    of the film, which specifies the sample value for each channel.
      *
      * \param weight
      *    Value to be added to the weight channel of the sample
      *
      * \param alpha
      *    Alpha value of the sample
      *
      * \param active
      *    Mask indicating if the lanes are active
      */
    virtual void prepare_sample(const UnpolarizedSpectrum &spec,
                                const Wavelength &wavelengths,
                                Float* aovs, Float weight = 1.f,
                                Float alpha = 1.f,
                                Mask active = true) const;

    /**
     * \brief Return an \ref ImageBlock instance, whose internal representation
     * is compatible with that of the film.
     *
     * Image blocks created using this method can later be merged into the
     * film using \ref put_block().
     *
     * \param size
     *   Desired size of the returned image block.
     *
     * \param normalize
     *    Force normalization of filter weights in \ref ImageBlock::put()?
     *    See the \ref ImageBlock constructor for details.
     *
     * \param border
     *    Should \c ImageBlock add an additional border region around around
     *    the image boundary? See the \ref ImageBlock constructor for details.
     */
    virtual ref<ImageBlock> create_block(const ScalarVector2u &size = 0,
                                         bool normalize = false,
                                         bool border = false) = 0;

    // =============================================================
    //! @{ \name Accessor functions
    // =============================================================

    /**
     * Should regions slightly outside the image plane be sampled to improve
     * the quality of the reconstruction at the edges? This only makes
     * sense when reconstruction filters other than the box filter are used.
     */
    bool sample_border() const { return m_sample_border; }

    /// Ignoring the crop window, return the resolution of the underlying sensor
    const ScalarVector2u &size() const { return m_size; }

    /// Return the size of the crop window
    const ScalarVector2u &crop_size() const { return m_crop_size; }

    /// Return the offset of the crop window
    const ScalarPoint2u &crop_offset() const { return m_crop_offset; }

    /**
     * \brief Set the size and offset of the film's crop window.
     *
     * The caller is responsible to invoke the parameters_changed() method on
     * any sensor referring to this film.
     *
     * This function will throw an exception if crop_offset + crop_size > size.
     *
     * \param crop_offset
     *    The offset of the crop window.
     *
     * \param crop_size
     *    The size of the crop window.
     */
    void set_crop_window(const ScalarPoint2u &crop_offset,
                         const ScalarVector2u &crop_size);

    /**
     * \brief Set the size of the film.
     *
     * This method will reset the crop window to the full image.
     *
     * The caller is responsible to invoke the parameters_changed() method on
     * any sensor referring to this film.
     *
     * \param size
     *     The new size of the film.
     */
    void set_size(const ScalarPoint2u &size);

    /// Return the image reconstruction filter (const version)
    const ReconstructionFilter *rfilter() const {
        return m_filter.get();
    }

    /// Returns the specific Sensor Response Function (SRF) used by the film
    const Texture *sensor_response_function();

    /// Flags for all properties combined.
    uint32_t flags() const { return m_flags; }

    //! @}
    // =============================================================

    virtual std::string to_string() const override;

    MI_DECLARE_CLASS()
protected:
    /// Create a film
    Film(const Properties &props);

    /// Virtual destructor
    virtual ~Film();

    /// Combined flags for all properties of this film.
    uint32_t m_flags;

protected:
    ScalarVector2u m_size;
    ScalarVector2u m_crop_size;
    ScalarPoint2u m_crop_offset;
    bool m_sample_border;
    ref<ReconstructionFilter> m_filter;
    ref<Texture> m_srf;
};

MI_EXTERN_CLASS(Film)
NAMESPACE_END(mitsuba)
